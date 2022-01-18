import numpy as np
import matplotlib.pyplot as plt

class mohrCircle():
    def __init__(self, sigX='none', sigY='none', tauXY='none'):
        self.sigX = sigX
        self.sigY = sigY
        self.tauXY = tauXY
        self.flag_phi = 0
        
        if self.sigX == 'none' or self.sigY == 'none' or self.tauXY == 'none':
            print('*** ERROR : please check all velues are properly entered ***')
    
    def cal_center(self):
        self.center = (self.sigX + self.sigY)/2
        return self.center
    
    def cal_R(self):
        R = np.sqrt(((self.sigX-self.sigY)/2)**2+self.tauXY**2)
        return R
    
    def cal_maxPstress(self):
        maxSig = self.cal_center()+self.cal_R()
        return maxSig

    def cal_minPstress(self): 
        minSig = self.cal_center() - self.cal_R()
        return minSig
    
    def cal_maxSstress(self):
        maxTau = self.cal_R()
        return maxTau
    
    def cal_minSstress(self):
        minTau = -self.cal_R()
        return minTau
    
    def cal_theta(self):
        theta = (np.arctan((2*self.tauXY)/(self.sigX-self.sigY))/2)*(180/np.pi)
        return theta
    
    def cal_4phi(self,phi='none'):
        self.flag_phi = 0
        #error 체크
        if type(phi) is str:
            print('원하는 각도를 degree로 입력해 주세요')
        else:
            angle = (self.cal_theta()+phi)*2
            self.phi = phi
            angle_rad = angle*(np.pi/180)
            self.flag_phi = 1
            
            #phi 에 대한 스트레스 계산
            sig1 = self.cal_center() + self.cal_R()*np.cos(angle_rad)
            tau1 = self.cal_R()*np.sin(angle_rad)
            self.sig1 = sig1
            self.tau1 = tau1
            
            return sig1, tau1
    
    def get_data(self):
        print('< ***** data ***** >')
        print('Center of Circle : %f' %self.cal_center())
        print('Radius of Circle : %f' %self.cal_R())
        print('theta : %f degree' %self.cal_theta())
        print('\n')
        
        print('< ***** Tensile Stress ***** >')
        print('Maximum Tensile Stress : %f' %self.cal_maxPstress())
        print('Minimum Tensile  Stress : %f' %self.cal_minPstress())
        print('\n')
        
        print('< ***** Shear Stress ***** >')
        print('Maximum Shear Stress : %f' %self.cal_maxSstress())
        print('Minimum Shear Stress : %f' %self.cal_minSstress())
        
        if self.flag_phi == 1:
            print('\n')
            print('\n')
            print('    < ***** data - Phi ***** >')
            print('    Phi : %f degree' %self.phi)
            print('\n')
            
            print('    < ***** Tesile Stress - Phi ***** >')
            print('    Tensile Stress 1 - Phi : %f' %self.sig1)
            print('    Tensile Stress 2 - Phi : %f' %(-self.sig1+2*self.center))
            print('\n')
            
            print('    < ***** Shear Stress - Phi ***** >')
            print('    Shear Stress 1 : %f' %self.tau1)
            print('    Shear Stress 2 : %f' %(-self.tau1))
        else:
            pass
        
    
    def plotCircle(self,figSize=[10,10]):
        rad = np.linspace(0,360,361)*(np.pi/180)
        
        #기본값
        sigpts = self.cal_center()+self.cal_R()*np.cos(rad)
        taupts = self.cal_R()*np.sin(rad)
        center = self.cal_center()
        R = self.cal_R()
        maxPS = self.cal_maxPstress()
        minPS = self.cal_minPstress()
        maxSS = self.cal_maxSstress()
        minSS = self.cal_minSstress()
        
        plt.figure(figsize = figSize)
        plt.plot(sigpts, taupts)
        plt.fill_between(sigpts, taupts, color = 'b', alpha = 0.1)
        
        #cross 표시
        plt.axhline(0, color = 'red', linewidth = 1)
        plt.axvline(center, color='red', linewidth = 1)
        
        #phi에 대한 line 표시
        if self.flag_phi == 1:
            #plt.plot([center,self.sig1],[0,self.tau1], color ='#39c5bb', linestyle = '--', linewidth = 2)
            plt.plot(self.sig1,self.tau1, color = '#39c5bb', marker = 'o')
            plt.text(self.sig1, self.tau1, '(%.2f,%.2f)' %(self.sig1,self.tau1), size = 10)
            
            plt.plot([-self.sig1+2*center,self.sig1],[-self.tau1,self.tau1], color ='#39c5bb', linestyle = '--', linewidth = 2, label = 'Specific Angle(phi)')
            
            #plt.plot([-self.sig1+2*center,center],[-self.tau1,0], color = '#39c5bb', linestyle = '--', linewidth = 2)
            plt.plot(-self.sig1+2*center, -self.tau1, color='#39c5bb', marker = 'o')
            plt.text(-self.sig1+2*center, -self.tau1, '(%.2f,%.2f)' %(-self.sig1+2*center,-self.tau1), size = 10)
        else:
            pass
        
        #maxminTau
        plt.plot(center,R, color = 'b', marker = 'o')
        plt.text(center,R,'(%.2f,%.2f)' %(center,R), size = 10)
        
        plt.plot(center, -R, color = 'b', marker = 'o')
        plt.text(center,-R,'(%.2f,%.2f)' %(center,-R), size = 10)
        
        #maxminSigma
        plt.plot(maxPS,0, color = 'b', marker = 'o')
        plt.text(maxPS ,2,'(%.2f,0)' %maxPS, size = 10)
        plt.plot(minPS,0, color = 'b', marker = 'o')
        plt.text(minPS ,2,'(%.2f,0)' %minPS, size = 10)
        
        #original line and original point 표시
        plt.plot([self.sigX, self.sigY], [self.tauXY, -self.tauXY], color = 'red', linestyle = '--', linewidth = 2, label = 'Original data')
        
        plt.plot(self.sigX,self.tauXY, color = 'r', marker = 'o')
        plt.text(self.sigX,self.tauXY,'(%.2f,%.2f)' %(self.sigX,self.tauXY), size = 12)
        plt.plot(self.sigY,-self.tauXY, color = 'r', marker = 'o')
        plt.text(self.sigY, -self.tauXY,'(%.2f,%.2f)' %(self.sigY, -self.tauXY), size = 12)
        
        #center 표시
        plt.plot(center,0, color = 'b', marker = 'o')
        plt.text(center,2,'center : (%.2f,0)' %center, size = 12)
        
        plt.grid()
        
        #graph 기본 정보 표시
        plt.title('mohr\'s circle', size = '30')
        plt.xlabel(r'$\sigma$', size = 30)
        plt.ylabel(r'$\tau$', size = 30)
        plt.legend()
        
        plt.show()
        

if __name__ =='__main__':
    a = mohrCircle(-10,50,40)
    a.cal_4phi(30)
    a.plotCircle()
    a.get_data()