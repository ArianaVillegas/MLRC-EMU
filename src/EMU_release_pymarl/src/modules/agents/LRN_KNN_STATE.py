import numpy as np
from sklearn.neighbors import BallTree,KDTree
import os
import gc
import torch as th
import pickle
from sys import platform
import numpy as np
from components.PenalizationManager import PenalizationManager
import time
import json
import os
import yaml


SAVE_PATH = os.path.expanduser("~/pruebas/MLRC-EMU/results") 
yaml_file_path= os.path.expanduser("~/pruebas/MLRC-EMU/src/EMU_release_pymarl/src/config/algs/EMU_sc2.yaml")  # Cambia esto a la ruta deseada
json_file_path= os.path.expanduser("~/pruebas/MLRC-EMU/src/EMU_release_pymarl/src/config/algs/nombre.json")
# Mapeo de atol_memory a su respectiva letra
with open(json_file_path, "r") as file2:
    config2 = json.load(file2)
nombre_experiemnto = config2.get("experiment_name")

atol_mapping = {
    0.00000013: "A",
    0.000013: "B",
    0.0013: "C",
    0.013: "D"
}
# Leer el archivo YAML
with open(yaml_file_path, "r") as file:
    config = yaml.safe_load(file)

# Obtener valores del YAML
atol_memory = config.get("atol_memory")

memory_emb_type = config.get("memory_emb_type")

# Determinar la letra correspondiente a atol_memory
letter = atol_mapping.get(atol_memory, "X")  # "X" si el valor no está en la tabla

# Crear el identificador (Ejemplo: B2, C3, etc.)
experiment_id = f"{nombre_experiemnto}_{letter}{memory_emb_type}"

decididor_exp = config.get("decididor_exp")
guardar_exp = config.get("guardar_exp")





def inverse_distance(h, h_i, epsilon=1e-3):
    #return 1 / (th.dist(h, h_i) + epsilon)
    return 1 / ( np.linalg.norm( h - h_i ) + epsilon) # L2 Euclidean distance

class LRU_KNN_STATE:
    def __init__(self, capacity, state_dim, args, env_name, random_projection, state_embed_net=None):
        
        z_dim = args.emdqn_latent_dim

        self.env_name = env_name
        self.capacity = capacity
        self.n_agent= args.n_agents
        self.device = args.device
        self.flag_stats_norm = args.flag_stats_norm
        self.random_projection = random_projection
        self.state_embed_net = state_embed_net
        self.fixed_delta     = args.fixed_delta
        self.delta_cover_type = int(args.delta_cover_type)

        self.memory_emb_type  = int(args.memory_emb_type) # 1: random projection, 2: state itself

        self.atol  = args.atol_memory *  np.ones(1, dtype=np.float32)
        self.rtol  = args.rtol_memory *  np.ones(1, dtype=np.float32)
        self.atol_monitor = self.atol *  np.ones(1, dtype=np.float32)
        self.rtol_monitor = self.rtol *  np.ones(1, dtype=np.float32)
        self.mu_Ncall     = np.zeros(1, dtype=np.float32)
        self.mu_Nxi       = np.zeros(1, dtype=np.float32)
        self.mu_ratio_xi  = np.zeros(1, dtype=np.float32)
        self.z_dim = z_dim

        self.use_AEM = args.use_AEM
        self.args = args

        # node information
        self.states         = np.empty((capacity, z_dim), dtype = np.float32) # projected value (z)
        self.states_norm    = np.empty((capacity, z_dim), dtype = np.float32) # y = (x- mu)/sigma
        self.global_states  = np.empty((capacity, state_dim), dtype = np.float32) # global state

        self.z_mu           = np.zeros(self.z_dim, dtype = np.float32)
        self.z_sigma        = np.ones(self.z_dim,  dtype = np.float32)
        self.x_mu           = np.zeros(self.z_dim, dtype = np.float32)
        self.x_sigma        = np.ones(self.z_dim,  dtype = np.float32)
        self.x_mu_monitor    = self.x_mu
        self.x_sigma_monitor = self.x_sigma 

        self.q_values_decay = np.zeros(capacity, dtype = np.float32) # = H(phi(s))
        self.tg             = np.zeros(capacity, dtype = int) # time step        
        self.xi             = np.zeros(capacity, dtype = np.uint)        
        self.gamma          = args.gamma

        # cnt
        self.Ncall          = np.zeros(capacity, dtype = int) # the number of transition (call)
        self.Nxi            = np.zeros(capacity, dtype = int) # the number of optimal transition 
        #self.rcnt           = np.zeros(capacity, dtype = np.float32) # = H(phi(s))
        self.epsilon        = 0.001

        # obsolete
        self.kernel         = inverse_distance

        self.lru = np.zeros(capacity)
        self.curr_capacity = 0
        self.tm = 0.0
        self.tree = None
        self.addnum = 0
        self.buildnum = 256
        self.buildnum_max = 256
        self.bufpath = './buffer/%s'%self.env_name
        self.build_tree_times = 0
        self.build_tree = False
        # Instanciamos la clase de penalización
        self.penalization_manager = PenalizationManager()


        self.umbral_visitas = 50  # Cantidad de visitas antes de penalizar
        self.penalizacion_maxima = 0.5  # Penalización máxima posible
        self.beta_penalizacion = 0.1  # Controla la suavidad de la penalización
        self.agent_id = 0
        self.access_logs = {}  # Diccionario para registrar accesos
        # 🔹 Generar nombre del archivo SOLO UNA VEZ al inicio del experimento
        if not os.path.exists(SAVE_PATH):
             os.makedirs(SAVE_PATH)
        self.experiment_start_time = time.strftime("%Y%m%d_%H%M%S")  # AñoMesDía_HoraMinutoSegundo
        self.log_file = os.path.join(SAVE_PATH, f"EC_{experiment_id}_{self.experiment_start_time}.json")
        self.guardar_exp=guardar_exp 
        self.decididor_exp=decididor_exp

        if not os.path.exists(self.log_file):
            data = {
                "duracion": {"inicio": time.time(), "fin": None},
                "guardar_exp":guardar_exp,
                "decididor_exp":decididor_exp,
                "atol_memory" : atol_memory,
                "memory_emb_type":memory_emb_type

            }
            with open(self.log_file, "w") as json_file:
                json.dump(data, json_file, indent=4)
       
    def iniciarId(self , id , diccioanrio):
        self.access_logs=diccioanrio
        self.agent_id =id
    def update_states_norm(self):   
        if self.build_tree == False:
            return

        self.x_mu_monitor    = np.mean(self.states[:self.curr_capacity],axis=0)
        self.x_sigma_monitor = np.std(self.states[:self.curr_capacity] ,axis=0)
                  
        if self.flag_stats_norm == True:
            
            self.x_mu    = self.x_mu_monitor
            self.x_sigma = self.x_sigma_monitor

            for i in range(0, self.z_dim ):
                self.states_norm[:self.curr_capacity,i] = (self.states[:self.curr_capacity,i] - self.x_mu[i])/self.x_sigma[i]

            #.. compute states of state_norm
            self.z_mu    = np.mean(self.states_norm[:self.curr_capacity],axis=0)
            self.z_sigma = np.std(self.states_norm[:self.curr_capacity] ,axis=0)
            max_z_sigma  = max(self.z_sigma)            

            #.. tolerance update
            if self.delta_cover_type == 1:
                self.atol_monitor = np.power(2.0 * max_z_sigma, self.z_dim ) / self.capacity
                self.rtol_monitor = np.zeros(1, dtype = np.float32)
            elif self.delta_cover_type == 2:
                self.atol_monitor = np.power(2.0*3.0 * max_z_sigma, self.z_dim ) / self.capacity
                self.rtol_monitor = np.zeros(1, dtype = np.float32)

            if self.fixed_delta == False:
                self.atol = self.atol_monitor
                self.rtol = self.rtol_monitor
        else:
            self.states_norm = self.states
        
        
    
        #.. modified version ----------------------------------------------------------------------------------------------------------

    def aumento_de_penalizacion(self, ind):
        """Aplica una penalización si un estado ha sido visitado demasiadas veces."""
            
        penalizacion = self.penalization_manager.penalizacion_sigmoide_mejorada(self.Ncall[ind])

        return penalizacion
    
    def peek_modified_EC(self, key, value_decay, xit, modify, global_state, cur_time):
        with open(self.log_file, 'r') as f:
            data = json.load(f)
        # input: key: global state
        # input: Rt, xi, modify
        # output: H(key_hat), xi(key_hat) 

        if modify == False:
            checkpoint = 1

        if self.curr_capacity==0 or self.build_tree == False:
            data['duracion']["fin"]=time.time()

            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=4)
            return None, None, None

        dist, ind = self.tree.query([key], k=1) # pick nearest one # 1-1 projection? 
        # TO CHECK: how about building tree based on states_norm and query ind with vector_atol ??? 
        ind = ind[0][0]

        # normalization
        key_norm = ((key - self.x_mu) / self.x_sigma) # check element-wise operation
        bollea=np.allclose(self.states_norm[ind], key_norm, rtol=self.rtol, atol=self.atol )
        #print(bollea)
        #if np.allclose(key_embed_hat, key_embed, rtol=self.rtol, atol=self.atol ):
        if bollea:
            self.lru[ind] = self.tm # update its updated time            
            self.tm +=0.01
            if modify:
                self.Ncall[ind] += 1
                if xit == 1: 
                    self.Nxi[ind] += 1 # optimal transition
                
                if (self.xi[ind] == 0) and (xit == 1) and self.use_AEM : # memory shift
                    self.xi[ind]          = xit
                    self.states[ind]      = key
                    self.states_norm[ind] = key_norm                    
                    self.global_states[ind]  = global_state
                    self.q_values_decay[ind] = value_decay

                    if self.args.flag_memory_cnt_reset == True:
                        self.Ncall[ind]       = 1
                        self.Nxi[ind]         = 1
                    self.tg[ind]          = cur_time
                
                else: # update Qval (value_decay: current Return)
                    #decididor_exp: true
                    #guardar_exp: false

                    Nuevo_incentivo = th.tensor( self.aumento_de_penalizacion(ind), dtype=value_decay.dtype, device=value_decay.device)
                    value_decay_penalizado =  value_decay - Nuevo_incentivo  
                    #print("dalue decay",value_decay) 
                    #print("dalue decay",value_decay_penalizado) 
                    v1= value_decay_penalizado if self.guardar_exp else value_decay
                    #print("v1",v1)
                    v2=value_decay_penalizado if self.decididor_exp else value_decay 
                    #print ("v2" ,v2)     
                    #print("-----------------------------------------------")
                    if v2 > self.q_values_decay[ind]: 
                        self.q_values_decay[ind] = v1
                                    
            rcnt = float(self.Nxi[ind] / (self.Ncall[ind] + self.epsilon))
            data['duracion']["fin"]=time.time()
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=4)
            

            return self.q_values_decay[ind], float(self.xi[ind]), rcnt
        data['duracion']["fin"]=time.time()
        with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=4)
            


        return None, None, None


    def add_modified_EC(self, key, value_decay, xi, global_state, cur_time):
        if self.curr_capacity >= self.capacity:
            # find the LRU entry
            old_index = np.argmin(self.lru)
            self.states[old_index] = key
            self.states_norm[old_index] = (key - self.x_mu)/self.x_sigma # check element-wise operation
            self.q_values_decay[old_index] = value_decay
            self.global_states[old_index]  = global_state
            self.xi[old_index] = xi
            self.lru[old_index] = self.tm
            if xi == 1 and self.args.flag_init_desirability == True:
                self.Nxi[old_index]  = 1
            else:
                self.Nxi[old_index]  = 0
            self.Ncall[old_index] = 1
            self.tg[old_index] = cur_time
        else:
            self.states[self.curr_capacity] = key
            self.states_norm[self.curr_capacity] = (key - self.x_mu)/self.x_sigma # check element-wise operation
            self.global_states[self.curr_capacity]  = global_state
            self.q_values_decay[self.curr_capacity] = value_decay            
            self.xi[self.curr_capacity] = xi
            self.lru[self.curr_capacity] = self.tm
            if xi == 1  and self.args.flag_init_desirability == True:
                self.Nxi[self.curr_capacity]  = 1
            else:
                self.Nxi[self.curr_capacity]  = 0
            self.Ncall[self.curr_capacity] = 1
            self.tg[self.curr_capacity] = cur_time
            self.curr_capacity+=1
        self.tm += 0.01

    #.. original version ----------------------------------------------------------------------------------------------------------


    def add_modified_EC(self, key, value_decay, xi, global_state, cur_time):
        if self.curr_capacity >= self.capacity:
            # find the LRU entry
            old_index = np.argmin(self.lru)
            self.states[old_index] = key
            self.states_norm[old_index] = (key - self.x_mu)/self.x_sigma # check element-wise operation
            self.q_values_decay[old_index] = value_decay
            self.global_states[old_index]  = global_state
            self.xi[old_index] = xi
            self.lru[old_index] = self.tm
            if xi == 1 and self.args.flag_init_desirability == True:
                self.Nxi[old_index]  = 1
            else:
                self.Nxi[old_index]  = 0
            self.Ncall[old_index] = 1
            self.tg[old_index] = cur_time
        else:
            self.states[self.curr_capacity] = key
            self.states_norm[self.curr_capacity] = (key - self.x_mu)/self.x_sigma # check element-wise operation
            self.global_states[self.curr_capacity]  = global_state
            self.q_values_decay[self.curr_capacity] = value_decay            
            self.xi[self.curr_capacity] = xi
            self.lru[self.curr_capacity] = self.tm
            if xi == 1  and self.args.flag_init_desirability == True:
                self.Nxi[self.curr_capacity]  = 1
            else:
                self.Nxi[self.curr_capacity]  = 0
            self.Ncall[self.curr_capacity] = 1
            self.tg[self.curr_capacity] = cur_time
            self.curr_capacity+=1
        self.tm += 0.01

    #.. original version ----------------------------------------------------------------------------------------------------------
    def peek_EC(self, key, value_decay, modify):
        if modify == False:
            x = 1

        if self.curr_capacity==0 or self.build_tree == False:
            return None

        dist, ind = self.tree.query([key], k=1) # pick nearest one
        ind = ind[0][0]
                        
        if np.allclose(self.states[ind], key, rtol=self.rtol, atol=self.atol ):
            self.lru[ind] = self.tm # update its updated time
            self.tm +=0.01
            if modify:
                if value_decay > self.q_values_decay[ind]: # update Qval (value_decay: current Return)
                    self.q_values_decay[ind] = value_decay
            return self.q_values_decay[ind]
        #print self.states[ind], key

        return None

    def add_EC(self, key, value_decay):
        if self.curr_capacity >= self.capacity:
            # find the LRU entry
            old_index = np.argmin(self.lru)
            self.states[old_index] = key
            self.q_values_decay[old_index] = value_decay
            self.lru[old_index] = self.tm
        else:
            self.states[self.curr_capacity] = key
            self.q_values_decay[self.curr_capacity] = value_decay
            self.lru[self.curr_capacity] = self.tm
            self.curr_capacity+=1
        self.tm += 0.01
    #---------------------------------------------------------------------------------------------------------------------------------------
    def update_kdtree(self):
        if self.build_tree:
            del self.tree
        self.tree = KDTree(self.states[:self.curr_capacity])
        self.build_tree = True
        self.build_tree_times += 1
        if self.build_tree_times == 50:
            self.build_tree_times = 0
            gc.collect()

    def check_tolerance(self):
        return self.atol, self.rtol, self.x_mu, self.x_sigma, self.z_mu, self.z_sigma

    def check_Ncall(self):
        self.mu_Ncall = np.mean(self.Ncall[:self.curr_capacity])
        self.mu_Nxi   = np.mean(self.Nxi[:self.curr_capacity])

        ratio_xi = np.divide( self.Nxi[:self.curr_capacity], self.Ncall[:self.curr_capacity] ) # element-wise
        self.mu_ratio_xi = np.mean(ratio_xi)

        return self.mu_Ncall, self.mu_Nxi, self.mu_ratio_xi, self.curr_capacity

    def save_memory(self, savepath):
        if not os.path.exists('buffer'):
            os.makedirs('buffer')
        if not os.path.exists(self.bufpath):
            os.makedirs(self.bufpath)

        np.save(os.path.join(savepath, 'states'), self.states[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'q_values_decay'), self.q_values_decay[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'Ncall'), self.Ncall[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'Nxi'), self.Nxi[:self.curr_capacity] )
        #np.save(os.path.join(savepath, 'rnd_projection'), self.random_projection )
        np.save(os.path.join(savepath, 'states_norm'), self.states_norm[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'global_states'), self.global_states[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'tg'), self.tg[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'lru'), self.lru[:self.curr_capacity] )
        np.save(os.path.join(savepath, 'xi'), self.xi[:self.curr_capacity] )

    def save(self, action):
        if not os.path.exists('buffer'):
            os.makedirs('buffer')
        if not os.path.exists(self.bufpath):
            os.makedirs(self.bufpath)
        np.save(os.path.join(self.bufpath, 'states_%d'%action), self.states[:self.curr_capacity])
        np.save(os.path.join(self.bufpath, 'states_norm_%d'%action), self.states_norm[:self.curr_capacity])
        np.save(os.path.join(self.bufpath, 'q_values_decay_%d'%action), self.q_values_decay[:self.curr_capacity])
        np.save(os.path.join(self.bufpath, 'lru_%d'%action), self.lru[:self.curr_capacity])

    def knn_value(self, key, knn):
        knn = min(self.curr_capacity, knn)
        if self.curr_capacity==0 or self.build_tree == False:
            return 0.0, 0.0

        dist, ind = self.tree.query([key], k=knn)

        value = 0.0
        value_decay = 0.0
        for index in ind[0]:
            value_decay += self.q_values_decay[index]
            self.lru[index] = self.tm
            self.tm+=0.01

        q_decay = value_decay / knn

        return q_decay

    def load(self, action):
        try:
            assert(os.path.exists(self.bufpath))
            lru = np.load(os.path.join(self.bufpath, 'lru_%d.npy'%action))
            cap = lru.shape[0]
            self.curr_capacity = cap
            self.tm = np.max(lru) + 0.01
            self.buildnum = self.buildnum_max

            self.states[:cap] = np.load(os.path.join(self.bufpath, 'states_%d.npy'%action))
            self.states_norm[:cap] = np.load(os.path.join(self.bufpath, 'states_norm_%d.npy'%action))
            self.q_values_decay[:cap] = np.load(os.path.join(self.bufpath, 'q_values_decay_%d.npy'%action))
            self.lru[:cap] = lru
            #self.tree = KDTree(self.states[:self.curr_capacity])
            self.tree = KDTree(self.states_norm[:self.curr_capacity])
            print ("load %d-th buffer success, cap=%d" % (action, cap))
        except:
            print ("load %d-th buffer failed" % action)

    def update_states_norm_old(self):        
        self.x_mu_monitor    = np.mean(self.states[:self.curr_capacity],axis=0)
        self.x_sigma_monitor = np.std(self.states[:self.curr_capacity] ,axis=0)
                
        max_x_sigma = max(self.x_sigma_monitor)            
        #min_x_sigma = min(self.x_sigma) 

        self.atol_monitor = np.power(2.0 * max_x_sigma, self.z_dim ) / self.capacity
        self.rtol_monitor = np.zeros(1, dtype = np.float32)
        
        if self.flag_stats_norm == True:
            self.atol = self.atol_monitor
            self.rtol = self.rtol_monitor
            self.x_mu    = self.x_mu_monitor
            self.x_sigma = self.x_sigma_monitor
            for i in range(0, self.z_dim ):
                self.states_norm[:self.curr_capacity,i] = (self.states[:self.curr_capacity,i] - self.x_mu[i])/self.x_sigma[i]
        else:
            self.states_norm = self.states
