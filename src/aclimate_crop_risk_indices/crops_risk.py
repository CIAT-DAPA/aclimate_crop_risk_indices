import pandas as pd
import glob
import os
import multiprocessing
from aclimate_crop_risk_indices.aclimate_calculations import main
from tqdm import tqdm

class CropsRisk():

    def __init__(self, path, cores, crop, country):
        self.crop = crop
        self.path = path
        self.cores = cores
        self.country = country
        self.configurations = []
        self.loaded_scenarios = {}
        self.path_inputs_crop = os.path.join(path, country,"inputs", "cultivos", crop)
        self.path_outputs_stations = os.path.join(path, country,"outputs","prediccionClimatica", "resampling")
        self.path_outputs_crop = os.path.join(path, country,"outputs", "cultivos", crop)
        self.path_inputs_crop = self.verify_path_exists(self.path_inputs_crop)
        self.path_outputs_stations = self.verify_path_exists(self.path_outputs_stations)
        self.path_outputs_crop = self.create_path_if_not_exists(self.path_outputs_crop)

    def verify_path_exists(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist.")
        return path

    def create_path_if_not_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'created folder { path }')
        return path
    
    def read_configurations(self):

        if len(os.listdir(self.path_inputs_crop)) <= 0:
            raise FileNotFoundError(f"\nNo configurations found for crop")

        for folder_name in tqdm(os.listdir(self.path_inputs_crop), desc=f"Processing data config"):
            folder_path = os.path.join(self.path_inputs_crop, folder_name)
            
            if os.path.isdir(folder_path):

                config_file_path = os.path.join(folder_path, "crop_conf.csv")
                coordinates_file_path = os.path.join(folder_path, "coordenadas.csv")

                if not os.path.exists(config_file_path):
                    print(f"\nNo configuration found in the folder {folder_name}")
                    continue

                if not os.path.exists(coordinates_file_path):
                    print(f"\nNo coordinates found in the folder {folder_name}")
                    continue
                
                partes = folder_name.split("_")
                
                ws, cultivar, soil, frequency = partes[:4]

                try:
                    df = pd.read_csv(config_file_path, index_col=False)
                    df_coor = pd.read_csv(coordinates_file_path, index_col=False)

                    elevation = df_coor[df_coor['name'] == 'elev']['value'].iloc[0]

                    self.configurations.append({
                        "id_estacion": ws,
                        "id_cultivar": cultivar,
                        "id_soil": soil,
                        "frecuencia": frequency,
                        "df_configuracion": df,
                        "file_name": folder_name,
                        "elevation": elevation,
                    })
                except Exception as e:
                    print(f"\nError reading configuration in folder {folder_name}: {e}")

    def load_scenario(self, ws): 
        
        if ws not in self.loaded_scenarios:
            path_station = self.verify_path_exists(os.path.join(self.path_outputs_stations, ws))
            archivos_csv = glob.glob(os.path.join(path_station, '*.csv'))
            
            if len(archivos_csv) <= 0:
                raise FileNotFoundError(f"\nNo scenarios found for station {ws}")
            
            scenarios = {}
            for archivo in archivos_csv:
                nombre_archivo = os.path.basename(archivo)
                scenarios[nombre_archivo] = pd.read_csv(archivo)
            self.loaded_scenarios[ws] = scenarios

    def procesar(self, dato):
        try:
            self.load_scenario(dato["id_estacion"])

            result = main(self.loaded_scenarios[dato["id_estacion"]], dato["df_configuracion"], dato["id_estacion"], dato["id_cultivar"], dato["id_soil"], dato["elevation"])
            result.to_csv(os.path.join(self.path_outputs_crop, f"{dato['file_name']}.csv"), na_rep=-1, index=False)

        except Exception as e:
            print("Error:", e)

    def run(self):
        try:      
            self.read_configurations()
        except Exception as e:
            print("Error reading configurations: ", e)

        with multiprocessing.Pool(self.cores) as pool:
            pool.map(self.procesar, self.configurations)