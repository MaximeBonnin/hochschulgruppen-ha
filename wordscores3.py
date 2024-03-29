### WORDSCORES (LBG-2003)
### author: Thiago Marzagao
### contact: marzagao ddott 1 at osu ddott edu
 
import os
import numpy as np
import pandas as pd
 
ipath = 'C:/Users/User/Desktop/Uni/WiSe 22-23/Empirische Demokratieforschung/Seminar_Methoden_der_Analyse_politischer_Texte_und_ihre_Anwendung/python_code/hausarbeit/inputdata/' # folder containing the CSV files
opath = 'C:/Users/User/Desktop/Uni/WiSe 22-23/Empirische Demokratieforschung/Seminar_Methoden_der_Analyse_politischer_Texte_und_ihre_Anwendung/python_code/hausarbeit/outputdata/' # folder where output will be saved


# hardcode your reference cases and their scores
A_r = pd.DataFrame({'referenceCase1': 1.0, # these are just examples
                   # 'referenceCase2': 5.0, 
                   'referenceCase3': 10.0},
                   index = ['score'])


class Wordscores:
    def __init__(self, A_r: pd.DataFrame):
        self.A_r = A_r


    # create function to load and merge data
    def load_data(self, caseSet: list, path: str, cols: dict) -> pd.DataFrame:
        '''
        iterable, string, dict -&gt; pandas.DataFrame
        '''
        output = pd.DataFrame(columns = ['word'])
        for case in caseSet:
        
            # check if case is casename or filename
            if '.csv' not in case:
                case = case + '.csv'
    
            # load new data file
            newData = pd.read_csv(path + case,
                                usecols = [col for col in cols.keys()],
                                dtype = cols,
                                names = ['word', case.replace('.csv', '')],
                                header = None)
    
            # merge with previous data
            output = pd.merge(output, newData, on = 'word', how = 'outer')
            output = output.fillna(0) # kill NaNs
                            
        return output


    def load_reference_data(self): #TODO rename
        # load reference data
        self.F_wr = self.load_data(self.A_r.keys(), ipath, {0: 'S30', 2: 'float'})

        # compute p(r|w) = f_wr / sum(f_wr)_{for all r} | probability of reading text r when seeing word w
        self.P_wr = self.F_wr.iloc[:, 1:].div(self.F_wr.sum(axis = 1), axis = 0)
 
        # compute Sw and save to file | 
        self.S_w = pd.DataFrame(self.F_wr.word)
        self.S_w['score'] = self.P_wr.dot(self.A_r.T)
        self.S_w.to_csv(opath + 'wordscores.csv', index = False)
        # print(self.S_w)
        # return self.S_w


    def load_virgin_data(self): #TODO rename
        # load virgin data (every file in directory that is not in reference data)
        virginSet = [file for file in os.listdir(ipath) 
                    if file.replace('.csv', '') not in self.A_r.keys()]
        self.virginAbsFreq = self.load_data(virginSet, ipath, {0: 'S30', 1: 'int'})

        # frequency of each virgin text word, as a proportion of the total number of words in the virgin text
        self.F_wv = self.load_data(virginSet, ipath, {0: 'S30', 2: 'float'})
        # print(self.F_wv)

    
    def run(self):
        self.load_reference_data()
        self.load_virgin_data()


        # 1:1 merge Fwv with Sw (to discard all disjoint words)
        temp = pd.merge(self.F_wv, self.S_w, on = 'word', how = 'inner')
        
        # split filtered Sw
        cleanSw = pd.DataFrame(temp.score)
        
        # clean up filtered Fwv
        del temp['word']
        del temp['score']
        cleanFwv = temp
        
        # compute Sv = sum(Fwv * Sw)_{for all w}
        self.Sv = cleanFwv.T.dot(cleanSw)
        
        # compute transformed self.Sv
        self.Sv_t = (self.Sv - self.Sv.mean()) * (self.A_r.T.std() / self.Sv.std()) + self.Sv.mean()
        
        # compute Vv
        Vv = (cleanFwv * np.square((np.array(cleanSw) 
                                    - np.array(self.Sv.T)))).sum(axis = 0)
        
        # 1:1 merge absolute frequencies with Sw (to discard all disjoint words)
        temp = pd.merge(self.virginAbsFreq, self.S_w, on = 'word', how = 'inner')
        
        # compute N
        del temp['word']
        del temp['score']
        N = temp.sum(axis = 0)
        
        # compute standard errors and confidence intervals
        std_error = np.sqrt(Vv / N)
        self.lower = np.array(self.Sv).flatten() - np.array((1.96 * std_error))
        self.upper = np.array(self.Sv).flatten() + np.array((1.96 * std_error))
        
        # compute transformed confidence intervals
        self.lower_t = (np.array(self.lower) - np.array(self.Sv.mean())) \
                * np.array((self.A_r.T.std() / self.Sv.std())) \
                + np.array(self.Sv.mean())
        self.upper_t = (np.array(self.upper) - np.array(self.Sv.mean())) \
                * np.array((self.A_r.T.std() / self.Sv.std())) \
                + np.array(self.Sv.mean())
        return self.Sv_t

        
    def print_everything(self):
        # print everything
        print(f"{self.A_r=}")
        print(f"{self.F_wr=}")
        print(f"{self.F_wv=}")
        print(f"{self.P_wr=}")
        print(f"{self.P_wr=}")
        print(f'{self.S_w.sort_values(by=["score"], ascending=False).head(20)=}')

        temp = pd.merge(self.F_wr, self.S_w, on = 'word', how = 'inner')
        temp["max_weight"] = temp[["LINKE", "AFD", "SPD", "FDP", "Grüne", "CDU"]].max(axis=1)
        print(f"{temp.sort_values(by=['max_weight'], ascending=False).head(20)}")



    

        
        # save transformed estimates to file
        self.Sv_t.to_csv(opath + 'virginScores.csv', index_label = 'case')

  

def main():
    print("Ran as main.")

    RILE_SCORES = {
    "GRÜNE": (41113, 2.22, 2.95), # (party code, LR_economic, LR_social) 
    "LINKE": (41223, 0.7, 2.67),
    "SPD": (41320, 1.5, 4.53),
    "FDP": (41420, 5.99, 3.52),
    "CDU": (41521, 5.8, 6.37),
    "AFD": (41953, 9.06, 8.15)
    }

    A_r_econ = pd.DataFrame({'LINKE': RILE_SCORES["LINKE"][1],
                    'AFD': RILE_SCORES["AFD"][1],
                    #"Linke": RILE_SCORES["LINKE"][1],
                    "SPD": RILE_SCORES["SPD"][1],
                    "FDP": RILE_SCORES["FDP"][1],
                    "CDU": RILE_SCORES["CDU"][1],
                    "Grüne": RILE_SCORES["GRÜNE"][1]},
                    index = ['score'])

    W = Wordscores(A_r=A_r_econ)


    W = Wordscores(A_r=A_r_econ)

    print(W.run())
    W.print_everything()




if __name__ == "__main__":
    main()