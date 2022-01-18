import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

class tauc():
    def __init__(self, fname = 'none', R = '0.5', qLength = '1'):
        self.fname = fname
        self.R = np.float64(R)
        self.qLength = np.float64(qLength)
        self.dfTauc = pd.DataFrame(columns = ['E', '(ahv)^2'])
        self.aConst = 2.302585093
        self.flag_Tauc = 0
        #self.1stDerv = pd.DataFrame(columns=['E_1','(ahv)^2_1'])
        #self.1stDerv = pd.DataFrame(columns=['E_2','(ahv)^2_2'])
        
    def readCsv(self):
        dfData = pd.read_csv(self.fname)
        self.dfData = dfData.dropna(axis = 0)
        
        print(self.dfData)
        return dfData
    
    def calTauc (self):
        
        self.readCsv()
        
        for i in self.dfData.index:
            #print(i, self.dfData.iloc[i,0])
            tmp_E = 0
            tmp_ahv = 0
            
            #E 계산
            if self.dfData.iloc[i,0]>0:
                tmp_E = 1240/self.dfData.iloc[i,0]
            else:
                pass
            
            #ahv 계산
            if self.dfData.iloc[i,0]>0:
                tmp_abs = self.dfData.iloc[i,1]
                tmp_ahv = np.divide((self.aConst*tmp_abs),self.qLength)**self.R
            else:
                pass

            tmp_data = {'E':tmp_E, '(ahv)^2':tmp_ahv}
            self.dfTauc =  self.dfTauc.append(tmp_data,ignore_index=True)
        
        self.flag_Tauc = 1
        return self.dfTauc
        
    #tauc 2 csv
    def saveTaucCsv(self,fname = '0'):
        if fname == 0:
            print('파일 이름을 입력해주세요')
        else:
            self.calTauc()
            self.dfTauc.to_csv(fname+'.csv',index = False)
            
    #plot uvvis
    def pltUvvis(self,figSize = [10,10], name = 'Material Name'):
        
        wl = self.dfData.iloc[:,0].dropna(axis=0).to_list()
        ab = self.dfData.iloc[:,1].dropna(axis=0).to_list()
        
        #plt base
        plt.figure(figsize= figSize)
        plt.plot(wl,ab, label=name)
        plt.legend(fontsize = 18)
        plt.xlabel('Wavelength', size = 15)
        plt.ylabel('Absorbacne', size = 15)
        
        plt.show()
    

    def calEp(self):
        
        #print(self.dfTauc.iloc[0,0])
        #print(self.dfTauc.iloc[-1,0])
        
        x = np.linspace(self.dfTauc.iloc[0,0], self.dfTauc.iloc[-1,0], 5000)
        y = interp1d(self.dfTauc.iloc[:,0], savgol_filter(self.dfTauc.iloc[:,1], 51, 3))
        
        #print(x)
        #print(y)
        
        #1차 미분
        dy = np.diff(y(x), 1)
        dx = np.diff(x, 1)
        
        #print('dx: ', dx)
        #print('dy: ', dy)
        
        y_1d = interp1d(x[:-1], dy/dx)

        #2차 미분
        d2y = np.diff(y(x), 2)
        dx2 = 0.0001
        y_2d = interp1d(x[:-2], d2y/dx2)
        
        #2차 미분이 0이 되는점 찾기
        gradmax = 0 #그래디언트 기초 초기화
        x_0 = 0
        y_0 = 0

        
        for i in range(2, len(x[:-2])):
            grad = y_1d(x[:-2])[i]
            if grad > gradmax:
                gradmax = grad
            if np.allclose([y_2d(x[:-2])[i]], [0.], atol=0.001) and y(x)[i] > 0.1*np.amax(self.dfTauc.iloc[:,1]) and grad >= gradmax:
                x_0 = x[i]
                y_0 = y(x)[i]
                
        #extrapolate 선 계산
        
        m = y_1d(x_0)
        c = y_0 - m*x_0
        
        self.x_cross = (0 - c)/m
        gap = self.x_cross
        gaps = []
        gaps.append([self.fname, self.x_cross])

#plot tauc
    def pltTauc(self,figSize = [10,10], name = 'Material Name', autoPlt = True):
        if self.flag_Tauc == 0:
            print('do calTauc first')
        else:
            E = self.dfTauc.iloc[:,0].to_list()
            ahv = self.dfTauc.iloc[:,1].to_list()
            
            #plt base
            plt.figure(figsize= figSize)
            plt.plot(E,ahv, label = name, color = 'g')
            plt.legend(fontsize = 18)
            plt.xlabel('Energy', size = 15)
            plt.ylabel('(ahv)^%.2f' %self.R, size = 15)
            plt.plot(self.x_cross, 0, 'o', linewidth = 3, color ='#39c5bb')
            plt.text(self.x_cross,0,'(%.3f:%.3f)' %(self.x_cross,0))
            
            if autoPlt == True: 
                plt.show()
            else: 
                pass
    
'''
    def pltAll(self):
        self.pltTauc(autoPlt = False)
        #plt.axhline(0, color = 'red', linewidth = 1)
        
        plt.plot(self.x_cross, 0, 'o', linewidth = 3, color ='#39c5bb')
        plt.text(self.x_cross,0,'(%.3f:%.3f)' %(self.x_cross,0))
        plt.show()
        '''

if __name__ == '__main__':
    a = tauc('uvvis.csv')
    a.readCsv()
    a.calTauc()
    a.calEp()
    a.pltUvvis()
    a.pltTauc()


