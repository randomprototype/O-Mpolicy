import streamlit as st
import numpy as np
import sys
from scipy.integrate import dblquad
from scipy.integrate import quad
from scipy.integrate import tplquad
from PIL import Image

def main():
    #criando 3 colunas
    col1, col2, col3 = st.columns(3)
    foto = Image.open('foto.png')
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    
    st.title('POLÍTICAS DE MANUTENÇÃO BASEADAS NO MODELO DE DELAY TIME PARA SISTEMAS DE DIFÍCIL ACESSO')
    st.write("Selecione o modelo de manutenção você deseja fazer uso no menu ao lado esquerdo.") 
    
    menu = ["Página Inicial", "GWH", "WDN", "OWT"]
    choice = st.sidebar.selectbox("Selecionar Modelo", menu)
    
    if choice == menu[1]:
    
        st.header("POLÍTICA DE MANUTENÇÃO GWH")

        #criando 3 colunas
        col21, col22 = st.columns(2)
        foto = Image.open('GWH.PNG')
        #inserindo na coluna 2
        col21.image(foto, use_column_width=True)
        col22.write("S -> Abertura de janela de oportunidades")
        col22.write("T -> Intervalo máximo entre inspeções")
        
        st.write("A política de manutenção implementada representa uma evolução do modelo proposto por Alotaibi et al. [2023]. Esta evolução inclui a consideração da inadimplência nas ações de manutenção oportunas, para tornar o modelo de manutenção ainda mais realista. Isso reconhece que as inspeções oportunas podem não ser viáveis devido à indisponibilidade de sobressalentes.")
        st.write("Referência: ALOTAIBI, Naif M. et al. Modified-opportunistic inspection and the case of remote, groundwater well-heads. Reliability Engineering & System Safety, v. 237, p. 109389, 2023.")
   
        st.subheader("Insira os parâmetros abaixo")
        st.subheader("Parâmetros de custo")
        cp = st.number_input("Custo da manutenção preventiva", min_value = 0.0, value = 1.0) # custo da preventiva
        cf = st.number_input("Custo da manutenção corretiva", min_value = 0.0, value = 5.0) # custo de falha
        ci = st.number_input("Custo da inspeção planejada", min_value = 0.0, value = 0.5) # custo de inspeção planejada
        co = st.number_input("Custo da inspeção oportuna", min_value = 0.0, value = 0.01) # custo de insp oportuna
        st.subheader("Parâmetros de mecanismos de defeitos e falhas")
        mi_x = st.number_input("Taxa de chegada dos defeitos", min_value = 0.5, value = 2.0) # escala fraca
        mi_h = st.number_input("Taxa de chegada das falhas", min_value = 0.5, value = 1.0) # escala forte
        st.subheader("Outros parâmetros")
        mi_z = st.number_input("Taxa de chegada das oportunidades", min_value = 0.5, value = 1.0) # forma fraca
        p = st.number_input("Probabilidade de inadimplência", min_value = 0.0, max_value = 1.0, value = 0.2) # parâmetro de mistura
        st.subheader("Insira as variáveis de decisão abaixo")
        S=st.number_input("Abertura de janela de oportunidades", min_value = 0.000, max_value = 100.000, value = 0.316) #Limite inferior da janela de oportunidades
        T=st.number_input("Intervalo máximo entre inspeções", min_value = 0.000, max_value = 100.000, value = 2.000) #Limite inferior da janela de oportunidades
        
        st.subheader("Pressione o botão abaixo para rodar a aplicação")
        botao = st.button("RUN")

        if botao:
            #%% Funções
            def fx(x):
                return mi_x * np.exp(-mi_x * x)
            def fh(h):
                return mi_h * np.exp(-mi_h * h)
            def fz(z):
                return mi_z * np.exp(-mi_z * z)
            
            def PROB(S, T):
                def P1(S, T):
                    return dblquad(lambda h, x: fx(x) * fh(h), 0, S, lambda x: 0, lambda x: S-x)[0]
                def P2(S, T):
                    return dblquad(lambda h, x: fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), 0, S, lambda x: S-x, lambda x: T-x)[0]
                def P3(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def P4(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def P5(S, T):
                    return dblquad(lambda h, x: fx(x) * fh(h) * np.exp(-mi_z * (T - S)), 0, S, lambda x: T-x, lambda x: np.inf)[0]
                def P6(S, T):
                    return dblquad(lambda h, x: fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), S, T, lambda x: 0, lambda x: T-x)[0]
                def P7(S, T):
                    return dblquad(lambda h, x: fx(x) * fh(h) * np.exp(-mi_z * (T - S)), S, T, lambda x: T-x, lambda x: np.inf)[0]
                def P8(S, T):
                    return quad(lambda x: fx(x) * np.exp(-mi_z * (T - S)), T, np.inf)[0]
                def P9(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def P10(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def P11(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def P12(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def P13(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def P14(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def P15(S, T):
                    return (1-p) * dblquad(lambda z, x: fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def P16(S, T):
                    return (p) * dblquad(lambda z, x: fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def P17(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def P18(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def P19(S, T):
                    return (1-p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                def P20(S, T):
                    return (p) * tplquad(lambda z, h, x: fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                return P1(S, T) + P2(S, T) + P3(S, T) + P4(S, T) +  P5(S, T) + P6(S, T) + P7(S, T) + P8(S, T) + P9(S, T) + P10(S, T) + P11(S, T) + P12(S, T) + P13(S, T) +  P14(S, T) + P15(S, T) + P16(S, T) + P17(S, T) + P18(S, T) + P19(S, T) + P20(S, T)
            
            def COST(S, T):
                def C1(S, T):
                    return dblquad(lambda h, x: (cf) * fx(x) * fh(h), 0, S, lambda x: 0, lambda x: S-x)[0]
                def C2(S, T):
                    return dblquad(lambda h, x: (cf) * fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), 0, S, lambda x: S-x, lambda x: T-x)[0]
                def C3(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co + cp) * fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def C4(S, T):
                    return (p) * tplquad(lambda z, h, x: (cf) * fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def C5(S, T):
                    return dblquad(lambda h, x: (ci + cp) * fx(x) * fh(h) * np.exp(-mi_z * (T - S)), 0, S, lambda x: T-x, lambda x: np.inf)[0]
                def C6(S, T):
                    return dblquad(lambda h, x: (cf) * fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), S, T, lambda x: 0, lambda x: T-x)[0]
                def C7(S, T):
                    return dblquad(lambda h, x: (ci + cp) * fx(x) * fh(h) * np.exp(-mi_z * (T - S)), S, T, lambda x: T-x, lambda x: np.inf)[0]
                def C8(S, T):
                    return quad(lambda x: (ci) * fx(x) * np.exp(-mi_z * (T - S)), T, np.inf)[0]
                def C9(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co + cp) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def C10(S, T):
                    return (p) * tplquad(lambda z, h, x: (cf) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def C11(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co + cp) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def C12(S, T):
                    return (p) * tplquad(lambda z, h, x: (ci + cp) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def C13(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co + cp) * fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def C14(S, T):
                    return (p) * tplquad(lambda z, h, x: (ci + cp) * fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def C15(S, T):
                    return (1-p) * dblquad(lambda z, x: (co) * fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def C16(S, T):
                    return (p) * dblquad(lambda z, x: (ci) * fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def C17(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def C18(S, T):
                    return (p) * tplquad(lambda z, h, x: (cf) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def C19(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (co) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                def C20(S, T):
                    return (p) * tplquad(lambda z, h, x: (ci + cp) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                return C1(S, T) + C2(S, T) + C3(S, T) + C4(S, T) +  C5(S, T) + C6(S, T) + C7(S, T) + C8(S, T) + C9(S, T) + C10(S, T) + C11(S, T) + C12(S, T) + C13(S, T) +  C14(S, T) + C15(S, T) + C16(S, T) + C17(S, T) + C18(S, T) + C19(S, T) + C20(S, T)
            
            def LIFE(S, T):
                def L1(S, T):
                    return dblquad(lambda h, x: (x + h) * fx(x) * fh(h), 0, S, lambda x: 0, lambda x: S-x)[0]
                def L2(S, T):
                    return dblquad(lambda h, x: (x + h) * fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), 0, S, lambda x: S-x, lambda x: T-x)[0]
                def L3(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def L4(S, T):
                    return (p) * tplquad(lambda z, h, x: (x + h) * fx(x) * fh(h) * fz(z), 0, S, lambda x: S-x, lambda x: T-x, lambda x, h: 0, lambda x, h: (x + h)-S)[0]
                def L5(S, T):
                    return dblquad(lambda h, x: (T) * fx(x) * fh(h) * np.exp(-mi_z * (T - S)), 0, S, lambda x: T-x, lambda x: np.inf)[0]
                def L6(S, T):
                    return dblquad(lambda h, x: (x + h) * fx(x) * fh(h) * np.exp(-mi_z * ((x + h) - S)), S, T, lambda x: 0, lambda x: T-x)[0]
                def L7(S, T):
                    return dblquad(lambda h, x: (T) * fx(x) * fh(h) * np.exp(-mi_z * (T - S)), S, T, lambda x: T-x, lambda x: np.inf)[0]
                def L8(S, T):
                    return quad(lambda x: (T) * fx(x) * np.exp(-mi_z * (T - S)), T, np.inf)[0]
                def L9(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def L10(S, T):
                    return (p) * tplquad(lambda z, h, x: (x + h) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: x-S, lambda x, h: (x + h)-S)[0]
                def L11(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def L12(S, T):
                    return (p) * tplquad(lambda z, h, x: (T) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: x-S, lambda x, h: T-S)[0]
                def L13(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def L14(S, T):
                    return (p) * tplquad(lambda z, h, x: (T) * fx(x) * fh(h) * fz(z), 0, S, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: T-S)[0]
                def L15(S, T):
                    return (1-p) * dblquad(lambda z, x: (z + S) * fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def L16(S, T):
                    return (p) * dblquad(lambda z, x: (T) * fx(x) * fz(z), T, np.inf, lambda x: 0, lambda x: T-S)[0]
                def L17(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def L18(S, T):
                    return (p) * tplquad(lambda z, h, x: (x + h) * fx(x) * fh(h) * fz(z), S, T, lambda x: 0, lambda x: T-x, lambda x, h: 0, lambda x, h: x-S)[0]
                def L19(S, T):
                    return (1-p) * tplquad(lambda z, h, x: (z + S) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                def L20(S, T):
                    return (p) * tplquad(lambda z, h, x: (T) * fx(x) * fh(h) * fz(z), S, T, lambda x: T-x, lambda x: np.inf, lambda x, h: 0, lambda x, h: x-S)[0]
                return L1(S, T) + L2(S, T) + L3(S, T) + L4(S, T) +  L5(S, T) + L6(S, T) + L7(S, T) + L8(S, T) + L9(S, T) + L10(S, T) + L11(S, T) + L12(S, T) + L13(S, T) +  L14(S, T) + L15(S, T) + L16(S, T) + L17(S, T) + L18(S, T) + L19(S, T) + L20(S, T)
            
            def OTM(x):
                return COST(x[0], x[1])/LIFE(x[0], x[1])
    
            y = [S, T]
            taxadecusto = OTM(y)
            st.write("Taxa de custo: {:.3f}" .format(taxadecusto))
        
    if choice == menu[2]:
        
        st.header("POLÍTICA DE MANUTENÇÃO WDN")

        #criando 3 colunas
        col21, col22 = st.columns(2)
        foto = Image.open('WDN.PNG')
        #inserindo na coluna 2
        col21.image(foto, use_column_width=True)
        col22.write("K -> Número de inspeções")
        col22.write("\u0394 -> Intervalo entre inspeções")
        col22.write("T -> Idade de substituição preventiva")
        
        st.write("A política de manutenção implementada representa uma evolução do modelo proposto por Scarf et al. [2009]. Esta evolução inclui a consideração de diferentes modos de falha, tais como desgaste natural e processos de choques.")
        st.write("Referência: SCARF, Phil A. et al. An age-based inspection and replacement policy for heterogeneous components. IEEE Transactions on reliability, v. 58, n. 4, p. 641-648, 2009.")
        
        st.subheader("Insira os parâmetros abaixo")
        st.subheader("Parâmetros de custo")
        cp = st.number_input("Custo da manutenção preventiva", min_value = 0.0, value = 1.0) # custo da preventiva
        cf = st.number_input("Custo da manutenção corretiva", min_value = 0.0, value = 5.0) # custo de falha
        ci = st.number_input("Custo da inspeção", min_value = 0.0, value = 0.1) # custo de inspeção
        cn = st.number_input("Custo unitário da degradação natural (em estado defeituoso)", min_value = 0.0, value = 0.04) # custo de downtime por unidade de tempo
        cc = st.number_input("Custo unitário da degradação por choques (em estado defeituoso)", min_value = 0.0, value = 0.04) # custo de downtime por unidade de tempo
        st.subheader("Parâmetros de mecanismos de defeitos e falhas")
        n1 = st.number_input("Parâmetros de escala dos componentes fracos", min_value = 0.0, value = 0.3) # escala fraca
        n2 = st.number_input("Parâmetros de escala dos componentes fortes", min_value = 0.0, value = 3.0) # escala forte
        b1 = st.number_input("Parâmetro de forma dos componentes fracos", min_value = 1.0, max_value = 6.0, value = 3.0) # forma fraca
        b2 = st.number_input("Parâmetro de forma dos componentes fortes", min_value = 1.0, max_value = 6.0, value = 3.0) # forma forte
        a = st.number_input("Parâmetro de mistura", min_value = 0.0, max_value = 1.0, value = 0.05) # parâmetro de mistura
        l = st.number_input("Inverso da média do delay time", min_value = 0.1, value = 1.0) # inverso da média da distribuição do delay time
        u = st.number_input("Taxa de chegada de choques", min_value = 0.0, max_value = 2.0, value = 0.5) # taxa de chegada de choques
        st.subheader("Insira as variáveis de decisão abaixo")
        k=int(st.number_input("Número de inspeções", min_value = 0, max_value = 30, step = 1, value = 8)) #Número total de visitas
        d=st.number_input("Intervalo entre inspeções", min_value = 0.000, max_value = 5.000, value = 0.369) #Limite inferior da janela de oportunidades
        t=st.number_input("Idade de substituição preventiva", min_value = 0.000, max_value = 20.000, value = 3.248) #Limite inferior da janela de oportunidades
      
        y=[k,d,t]
      
        st.subheader("Pressione o botão abaixo para rodar a aplicação")
        botao = st.button("RUN")
        
        if botao:
            def otm(y):
                #DEGRADAÇÃO NATURAL
                def f01(x):#função de densidade da weibull para a chegada de defeitos advindos de uma degradação natural (para componentes fracos)
                    return (b1/n1)*((x/n1)**(b1-1))*np.exp(-(x/n1)**b1)
                def f02(x): #função de densidade da weibull para a chegada de defeitos advindos de uma degradação natural (para componentes fortes)
                    return (b2/n2)*((x/n2)**(b2-1))*np.exp(-(x/n2)**b2)
                def fx(x): #função de mistura das distribuições
                    return (a*f01(x))+((1-a)*f02(x))
                def Fx(t): #função de densidade da weibull para a chegada de defeitos advindos de uma degradação natural
                    Fx,_ = quad(lambda x: fx(x), 0, t)
                    return Fx
                def Rx(t): #função de confiabilidade da weibull para a chegada de defeitos advindos de uma degradação natural
                    Rx,_ = quad(lambda x: fx(x), t, np.inf)
                    return Rx
                #CHOQUES
                def fz(z): #função de densidade da exponencial para a chegada do choque
                    return u*np.exp(-u*z)
                def Fz(z): #função acumulada da exponencial para a chegada do choque
                    return 1-np.exp(-u*z)
                def Rz(z): #função confiabilidade da exponencial para a chegada do choque
                    return np.exp(-u*z)
                #DELAY-TIME  
                def fh(h): #função de densidade da exponencial para o tamanho do delay-time
                    return l*np.exp(-l*h)
                def Fh(h): #função acumulada da exponencial para o tamanho do delay-time
                    return 1-np.exp(-l*h)
                def Rh(h): #função confiabilidade da exponencial para o tamanho do delay-time
                    return np.exp(-l*h)
            
                #FUNÇÃO CUSTO DE CADA CENÁRIO
                def fc1(h):
                  return (cf+ci*(i-1)+cn*(h))
                def fc2(x):
                  return (cp+ci*(i)+cn*(i*D-x))
                def fc3(h):
                  return (cf+ci*(K)+cn*(h))
                def fc4(x):
                  return (cp+ci*(K)+cn*(T-x))
                def fc5(h):
                  return (cf+ci*(i-1)+cc*(h))
                def fc6(z):
                  return (cp+ci*(i)+cc*(i*D-z))
                def fc7(h):
                  return (cf+ci*(K)+cc*(h))
                def fc8(z):
                  return (cp+ci*(K)+cc*(T-z))
                def fc9():
                  return (cp+ci*(K))
            
                #FUNÇÃO VIDA DE CADA CENÁRIO
                def fv1(x, h):
                  return (x+h)
                def fv2():
                  return (i*D)
                def fv3(x, h):
                  return (x+h)
                def fv4():
                  return (T)
                def fv5(z, h):
                  return (z+h)
                def fv6():
                  return (i*D)
                def fv7(z, h):
                  return (z+h)
                def fv8():
                  return (T)
                def fv9():
                  return (T)
            
            
                #Variáveis de decisão
                K = y[0] #número de inspeções
                D = y[1] #intervalo entre inspeções
                T = y[2] #idade de substituição preventiva
            
                #Variáveis de auxílio
                sc = sv = prob1 = prob2 = prob3 = prob4 = prob5 = prob6 = prob7 = prob8 = prob9 = tam1 = tam2 = tam3 = tam4 = tam5 = tam6 = tam7 = tam8 = tam9 = cust1 = cust2 = cust3 = cust4 = cust5 = cust6 = cust7 = cust8 = cust9 = 0
            
                #CENÁRIOS
                #CASO 01#######################################################################################################################################################################################################################
                for i in range(1, K+1):
                    p1,_=quad(lambda x: (Rz(x)*fx(x)*Fh(i*D-x)), (i-1)*D, i*D)
                    c1,_=dblquad(lambda h, x: (fc1(h)*Rz(x)*fx(x)*fh(h)), (i-1)*D, i*D, lambda x: 0, lambda x: i*D-x)
                    t1,_=dblquad(lambda h, x: (fv1(x, h)*Rz(x)*fx(x)*fh(h)), (i-1)*D, i*D, lambda x: 0, lambda x: i*D-x)
                    
                    cust1 = cust1 + c1
                    tam1 = tam1 + t1
                    prob1 = prob1 + p1
            
                    sc = sc + c1
                    sv = sv + t1
            
                #CASO 02#######################################################################################################################################################################################################################
                for i in range(1, K+1):
                    p2,_=quad(lambda x: (Rz(x)*fx(x)*Rh(i*D-x)), (i-1)*D, i*D)
                    c2,_=quad(lambda x: (fc2(x)*Rz(x)*fx(x)*Rh(i*D-x)), (i-1)*D, i*D)
                    t2,_=quad(lambda x: (fv2()*Rz(x)*fx(x)*Rh(i*D-x)), (i-1)*D, i*D)
                    
                    cust2 = cust2 + c2
                    tam2 = tam2 + t2
                    prob2 = prob2 + p2
            
                    sc = sc + c2
                    sv = sv + t2
            
                #CASO 03#######################################################################################################################################################################################################################
                p3,_=quad(lambda x: (Rz(x)*fx(x)*Fh(T-x)), K*D, T)
                c3,_=dblquad(lambda h, x: (fc3(h)*Rz(x)*fx(x)*fh(h)), K*D, T, lambda x: 0, lambda x: T-x)
                t3,_=dblquad(lambda h, x: (fv3(x, h)*Rz(x)*fx(x)*fh(h)), K*D, T, lambda x: 0, lambda x: T-x)
                
                cust3 = cust3 + c3
                tam3 = tam3 + t3
                prob3 = prob3 + p3
            
                sc = sc + c3
                sv = sv + t3
            
                #CASO 04#######################################################################################################################################################################################################################
                p4,_=quad(lambda x: (Rz(x)*fx(x)*Rh(T-x)), K*D, T)
                c4,_=quad(lambda x: (fc4(x)*Rz(x)*fx(x)*Rh(T-x)), K*D, T)
                t4 = fv4()*p4
                
                cust4 = cust4 + c4
                tam4 = tam4 + t4
                prob4 = prob4 + p4
            
                sc = sc + c4
                sv = sv + t4
            
                #CASO 05#######################################################################################################################################################################################################################
                for i in range(1, K+1):
                    p5,_=quad(lambda z: (fz(z)*Rx(z)*Fh(i*D-z)), (i-1)*D, i*D)
                    c5,_=dblquad(lambda h, z: (fc5(h)*Rx(z)*fz(z)*fh(h)), (i-1)*D, i*D, lambda z: 0, lambda z: i*D-z)
                    t5,_=dblquad(lambda h, z: (fv5(z, h)*Rx(z)*fz(z)*fh(h)), (i-1)*D, i*D, lambda z: 0, lambda z: i*D-z)
                    
                    cust5 = cust5 + c5
                    tam5 = tam5 + t5
                    prob5 = prob5 + p5
            
                    sc = sc + c5
                    sv = sv + t5
                
                #CASO 06#######################################################################################################################################################################################################################
                for i in range(1, K+1):
                    p6,_=quad(lambda z: (fz(z)*Rx(z)*Rh(i*D-z)), (i-1)*D, i*D)
                    c6,_=quad(lambda z: (fc6(z)*fz(z)*Rx(z)*Rh(i*D-z)), (i-1)*D, i*D)
                    t6,_=quad(lambda z: (fv6()*fz(z)*Rx(z)*Rh(i*D-z)), (i-1)*D, i*D)
                    
                    cust6 = cust6 + c6
                    tam6 = tam6 + t6
                    prob6 = prob6 + p6
            
                    sc = sc + c6
                    sv = sv + t6
                
                #CASO 07#######################################################################################################################################################################################################################
                p7,_=quad(lambda z: (fz(z)*Rx(z)*Fh(T-z)), K*D, T)
                c7,_=dblquad(lambda h, z: (fc7(h)*fz(z)*Rx(z)*fh(h)), K*D, T, lambda z: 0, lambda z: T-z)
                t7,_=dblquad(lambda h, z: (fv7(z, h)*fz(z)*Rx(z)*fh(h)), K*D, T, lambda z: 0, lambda z: T-z)
                
                cust7 = cust7 + c7
                tam7 = tam7 + t7
                prob7 = prob7 + p7
            
                sc = sc + c7
                sv = sv + t7
            
                #CASO 08#######################################################################################################################################################################################################################
                p8,_=quad(lambda z: (fz(z)*Rx(z)*Rh(T-z)), K*D, T)
                c8,_=quad(lambda z: (fc8(z)*fz(z)*Rx(z)*Rh(T-z)), K*D, T)
                t8 = fv8()*p8
                
                cust8 = cust8 + c8
                tam8 = tam8 + t8
                prob8 = prob8 + p8
            
                sc = sc + c8
                sv = sv + t8
            
                #CASO 09#######################################################################################################################################################################################################################
                p9 = Rz(T)*Rx(T)
                c9 = fc9()*p9
                t9 = fv9()*p9
                
                cust9 = cust9 + c9
                tam9 = tam9 + t9
                prob9 = prob9 + p9
            
                sc = sc + c9
                sv = sv + t9

                tc = sc/sv
                return tc
            
            taxadecusto = otm(y)
            st.write("Taxa de custo: {:.3f}" .format(taxadecusto))

    if choice == menu[3]:
          
        st.header("POLÍTICA DE MANUTENÇÃO OWT")
        
        #criando 3 colunas
        col21, col22 = st.columns(2)
        foto = Image.open('OWT.PNG')
        #inserindo na coluna 2
        col21.image(foto, use_column_width=True)
        col22.write("K -> Número de inspeções")
        col22.write("s -> Intervalo entre visitas")
        col22.write("Ws -> Abertura da janela de oportunidades")
        col22.write("Ms -> Idade de substituição preventiva")
        
        st.write("A política de manutenção implementada representa uma evolução do modelo proposto por Melo et al. [2023]. Esta evolução inclui a consideração de outros critérios de decisão para avaliar qual o impacto destes novos critérios na definição da política de manutenção.")
        st.write("Referência: MELO, Yan R. et al. A hybrid maintenance policy with fixed periodic structure and opportunistic replacement. Proceedings of the Institution of Mechanical Engineers, Part O: Journal of Risk and Reliability, v. 237, n. 3, p. 579-591, 2023.")
        
        st.subheader("Insira os parâmetros abaixo")
        st.subheader("Parâmetros de custo")
        cp = st.number_input("Custo da manutenção preventiva", min_value = 0.0, value = 1.0) # custo da preventiva
        cf = st.number_input("Custo da manutenção corretiva", min_value = 0.0, value = 2.0) # custo de falha
        co = st.number_input("Custo de manutenção oportuna", min_value = 0.0, value = 0.5) # custo de oportunidade
        ci = st.number_input("Custo da inspeção", min_value = 0.0, value = 0.05) # custo de inspeção
        cd = st.number_input("Custo de downtime por unidade de tempo", min_value = 0.0, value = 0.1) # custo de downtime por unidade de tempo
        st.subheader("Parâmetros de mecanismos de defeitos e falhas")
        a1 = st.number_input("Parâmetros de escala dos componentes fracos", min_value = 0.0, value = 1.0) # escala fraca
        a2 = st.number_input("Parâmetros de escala dos componentes fortes", min_value = 0.0, value = 10.0) # escala forte
        b1 = st.number_input("Parâmetro de forma dos componentes fracos", min_value = 1.0, max_value = 6.0, value = 2.0) # forma fraca
        b2 = st.number_input("Parâmetro de forma dos componentes fortes", min_value = 1.0, max_value = 6.0, value = 2.0) # forma forte
        r = st.number_input("Parâmetro de mistura", min_value = 0.0, max_value = 1.0, value = 0.05) # parâmetro de mistura
        l = st.number_input("Inverso da média do delay time", min_value = 0.1, value = 1.0) # inverso da média da distribuição do delay time
        st.subheader("Outros parâmetros")
        u = st.number_input("Taxa de chegada de oportunidades", min_value = 0.0, max_value = 2.0, value = 0.25) # taxa de chegada de choques
        s = st.number_input("Intervalo de tempo entre visitas", min_value = 0.0, value = 1.0) #intervalo entre visitas
        p = st.number_input("Probabilidade de default", min_value = 0.0, max_value = 1.0, value = 0.2) #probabilidade de default
        st.subheader("Insira as variáveis de decisão abaixo")
        k=int(st.number_input("Número de inspeções", min_value = 0, max_value = 10, step = 1, value = 1)) #Número total de visitas
        W=int(st.number_input("Visita de abertura da janela de oportunidades", min_value = 0, max_value = 15, step = 1, value = 6)) #Limite inferior da janela de oportunidades
        M=int(st.number_input("Visita de idade de substituição preventiva", min_value = 0, max_value = 40, step = 1, value = 10)) #Limite inferior da janela de oportunidades
        
        st.subheader("Pressione o botão abaixo para rodar a aplicação")
        botao = st.button("RUN")
        
        if botao:
            def otm(y1, y2, y3):
                def f01(x):#weibull density func (for weak comp) for arrival of defects
                    return (b1/a1)*((x/a1)**(b1-1))*np.exp(-(x/a1)**b1)
                def f02(x):#weibull density func (for strong comp) for arrival of defects
                    return (b2/a2)*((x/a2)**(b2-1))*np.exp(-(x/a2)**b2)
                def fx(x):#mixing of distributions
                    return r*f01(x)+(1-r)*f02(x)
                def fh(h):#exponencial density func for delay time
                    return l*np.exp(-l*h)
                def Fh(h):#exponencial culmulative func for delay time
                    return 1-np.exp(-l*h)
            
                #Variáveis de Decisão
                k = y1
                M = y3
                W = y2
            
                #Variáveis de auxílio
                sc = sv = pr = dt = pt = 0
            
                prob1 = prob2 = prob3 = prob4 = prob5 = prob6 = prob7 = prob8 = prob9 = prob10 = 0
                prob11 = prob12 = prob13 = prob14 = prob15 = prob16 = prob17 = prob18 = prob19 = prob20 = 0
                prob21 = prob22 = prob23 = prob24 = prob25 = prob26 = prob27 = prob28 = prob29 = prob30 = 0
                prob31 = prob32 = prob33 = prob34 = prob35 = prob36 = prob37 = prob38 = prob39 = prob40 = 0
                prob41 = 0
            
                down1 = down2 = down3 = down4 = down5 = down6 = down7 = down8 = down9 = down10 = 0
                down11 = down12 = down13 = down14 = down15 = down16 = down17 = down18 = down19 = down20 = 0
                down21 = down22 = down23 = down24 = down25 = down26 = down27 = down28 = down29 = down30 = 0
                down31 = down32 = down33 = down34 = down35 = down36 = down37 = down38 = down39 = down40 = 0
                down41 = 0
            
                tam1 = tam2 = tam3 = tam4 = tam5 = tam6 = tam7 = tam8 = tam9 = tam10 = 0
                tam11 = tam12 = tam13 = tam14 = tam15 = tam16 = tam17 = tam18 = tam19 = tam20 = 0
                tam21 = tam22 = tam23 = tam24 = tam25 = tam26 = tam27 = tam28 = tam29 = tam30 = 0
                tam31 = tam32 = tam33 = tam34 = tam35 = tam36 = tam37 = tam38 = tam39 = tam40 = 0
                tam41 = 0
            
                cust1 = cust2 = cust3 = cust4 = cust5 = cust6 = cust7 = cust8 = cust9 = cust10 = 0
                cust11 = cust12 = cust13 = cust14 = cust15 = cust16 = cust17 = cust18 = cust19 = cust20 = 0
                cust21 = cust22 = cust23 = cust24 = cust25 = cust26 = cust27 = cust28 = cust29 = cust30 = 0
                cust31 = cust32 = cust33 = cust34 = cust35 = cust36 = cust37 = cust38 = cust39 = cust40 = 0
                cust41 = 0
            
                probt1 = probt2 = probt3 = probt4 = probt5 = probt6 = probt7 = probt8 = probt9 = probt10 = 0
                probt11 = probt12 = probt13 = probt14 = probt15 = probt16 = probt17 = probt18 = probt19 = probt20 = 0
                probt21 = probt22 = probt23 = probt24 = probt25 = probt26 = probt27 = probt28 = probt29 = probt30 = 0
                probt31 = probt32 = probt33 = probt34 = probt35 = probt36 = probt37 = probt38 = probt39 = probt40 = 0
                probt41 = 0
            
                ##CASOS
            
                ###############################################CASO 1
                #O defeito e a falha ocorrem na fase de inspeção
                def fd1(h,x): #Caso 1
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt1(h,x): #Caso 1
                    return ((fh(h))*(fx(x)))
            
                #CASO 1
                for i in range(1, k+1):
                    pt1,_=dblquad(fpt1, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                    d1,_=dblquad(fd1, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                
                    c1=pt1*(1-p)*((i-1)*ci+cf)
                    t1=pt1*(1-p)*(i*s)
                    d1=d1*(1-p)
                    pt1=pt1*(1-p)
                    
                    cust1 = cust1 + c1
                    tam1 = tam1 + t1
                    down1 = down1 + d1
                    probt1 = probt1 + pt1
                
                    sc = sc + c1
                    sv = sv + t1
                    dt = dt + d1
                    pt = pt + pt1
            
                ###############################################CASO 2
                def fd2(h,x): #Caso 2
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt2(h,x): #Caso 2
                    return ((fh(h))*(fx(x)))
            
                #CASO 2
                if W >= k+1:
                    lim = k+1
                if W == k:
                    lim = k
            
                for i in range(2, lim+1):
                    d2,_=dblquad(fd2, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                    pt2,_=dblquad(fpt2, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                    
                    c2=pt2*(p)*((i-1)*ci+cf)
                    t2=pt2*(p)*(i*s)
                    d2=d2*(p)
                    pt2=pt2*(p)
                        
                    cust2 = cust2 + c2
                    tam2 = tam2 + t2
                    down2 = down2 + d2
                    probt2 = probt2 + pt2
                    
                    sc = sc + c2
                    sv = sv + t2
                    dt = dt + d2
                    pt = pt + pt2
            
                ###############################################CASO 3
                def fd3(h,x): #Caso 3
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt3(h,x): #Caso 3
                    return ((fh(h))*(fx(x)))
            
                #CASO 3   
                for i in range(2, k+1):
                    d3,_=dblquad(fd3, (i-2)*s, (i-1)*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                    pt3,_=dblquad(fpt3, (i-2)*s, (i-1)*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                    
                    c3=pt3*(p)*((i-1)*ci+cf)
                    t3=pt3*(p)*(i*s)
                    d3=d3*(p) 
                    pt3=pt3*(p)
                    
                    cust3 = cust3 + c3
                    tam3 = tam3 + t3
                    down3 = down3 + d3    
                    probt3 = probt3 + pt3
                    
                    sc = sc + c3
                    sv = sv + t3
                    dt = dt + d3
                    pt = pt + pt3
            
                ###############################################CASO 4
                def fd4(h,x): #Caso 4
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt4(h,x): #Caso 4
                    return ((fh(h))*(fx(x)))
            
                #CASO 4
                if k >= 1:
                    for i in range(k+1, W+1):
                        d4,_=dblquad(fd4, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                        pt4,_=dblquad(fpt4, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                            
                        c4=pt4*(p)*(k*ci+cf)
                        t4=pt4*(p)*(i*s)
                        d4=d4*(p)
                        pt4=pt4*(p)
                        
                        cust4 = cust4 + c4
                        tam4 = tam4 + t4
                        down4 = down4 + d4
                        probt4 = probt4 + pt4
                        
                        sc = sc + c4
                        sv = sv + t4
                        dt = dt + d4
                        pt = pt + pt4
            
                ###############################################CASO 5
                def fd5(h,x): #Caso 5
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt5(h,x): #Caso 5
                    return ((fh(h))*(fx(x)))
            
                #CASO 5
                if W <= M-1:
                    lim = W
                else:
                    lim = M-1
                
                for i in range(k+2, lim+1):
                    for j in range(k+1, i):
                        d5,_=dblquad(fd5, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                        pt5,_=dblquad(fpt5, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                        
                        c5=pt5*(1-p)*(k*ci+cf)
                        t5=pt5*(1-p)*(i*s)
                        d5=d5*(1-p)
                        pt5=pt5*(1-p)
                            
                        cust5 = cust5 + c5
                        tam5 = tam5 + t5
                        down5 = down5 + d5        
                        probt5 = probt5 + pt5
                        
                        sc = sc + c5
                        sv = sv + t5
                        dt = dt + d5
                        pt = pt + pt5
                
                ###############################################CASO 6
                def fd6(h,x): #Caso 6
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt6(h,x): #Caso 6
                    return ((fh(h))*(fx(x)))
            
                #CASO 6
                for i in range(k+3, W+1):
                    for j in range(k+1, i-1):
                        d6,_=dblquad(fd6, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x)
                        pt6,_=dblquad(fpt6, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x)
                        
                        c6=pt6*(p)*(k*ci+cf)
                        t6=pt6*(p)*(i*s)
                        d6=d6*(p)
                        pt6=pt6*(p)
                            
                        cust6 = cust6 + c6
                        tam6 = tam6 + t6
                        down6 = down6 + d6        
                        probt6 = probt6 + pt6
                            
                        sc = sc + c6
                        sv = sv + t6
                        dt = dt + d6
                        pt = pt + pt6
            
                ###############################################CASO 7
                def fd7(h,x): #Caso 7
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt7(h,x): #Caso 7
                    return ((fh(h))*(fx(x)))
            
                #CASO 7
                if W <= M-1:
                    lim = W
                else:
                    lim = M-1
                    
                for i in range(k+1, lim+1):
                    d7,_=dblquad(fd7, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                    pt7,_=dblquad(fpt7, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                        
                    c7=pt7*(1-p)*(k*ci+cf)
                    t7=pt7*(1-p)*(i*s)
                    d7=d7*(1-p)
                    pt7=pt7*(1-p)
                        
                    cust7 = cust7 + c7
                    tam7 = tam7 + t7
                    down7 = down7 + d7           
                    probt7 = probt7 + pt7
                        
                    sc = sc + c7
                    sv = sv + t7
                    dt = dt + d7
                    pt = pt + pt7
            
                ###############################################CASO 8
                def fd8(h,x): #Caso 8
                    return ((i*s-(x+h))*(fh(h))*(fx(x)))
                def fpt8(h,x): #Caso 8
                    return ((fh(h))*(fx(x)))
            
                #CASO 8
                for i in range(k+2, W+1):
                    d8,_=dblquad(fd8, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                    pt8,_=dblquad(fpt8, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                    
                    c8=pt8*(p)*(k*ci+cf)
                    t8=pt8*(p)*(i*s)
                    d8=d8*(p)
                    pt8=pt8*(p)
                    
                    cust8 = cust8 + c8
                    tam8 = tam8 + t8
                    down8 = down8 + d8     
                    probt8 = probt8 + pt8
                    
                    sc = sc + c8
                    sv = sv + t8
                    dt = dt + d8
                    pt = pt + pt8
                
                ###############################################CASO 9
                def fpt9(h,x): #Caso 9
                    return ((fh(h))*(fx(x)))
            
                #CASO 9
                for i in range(1, k+1):
                    pt9,_=dblquad(fpt9, (i-1)*s, i*s, lambda x: i*s-x, lambda x: np.inf)
                    
                    c9=pt9*(1-p)*(i*ci+cp)
                    t9=pt9*(1-p)*(i*s)
                    pt9=pt9*(1-p)
                    
                    cust9 = cust9 + c9
                    tam9 = tam9 + t9   
                    probt9 = probt9 + pt9
                    
                    sc = sc + c9
                    sv = sv + t9
                    pt = pt + pt9
                    
                ###############################################CASO 10
                def fpt10(h,x): #Caso 10
                    return ((fh(h))*(fx(x)))
            
                #CASO 10
                for i in range(2, k+1):
                    pt10,_=dblquad(fpt10, (i-2)*s, (i-1)*s, lambda x: i*s-x, lambda x: np.inf)
                    
                    c10=pt10*(p)*(i*ci+cp)
                    t10=pt10*(p)*(i*s)
                    pt10=pt10*(p)
                    
                    cust10 = cust10 + c10
                    tam10 = tam10 + t10  
                    probt10 = probt10 + pt10
                
                    sc = sc + c10
                    sv = sv + t10
                    pt = pt + pt10
                    
                ###############################################CASO 11
                def fd11(h,x): #Caso 11
                    return (((k+1)*s-(x+h))*(np.exp(-u*(((k+1)*s)-(k*s))))*(fh(h))*(fx(x)))
                def fpt11(h,x): #Caso 11
                    return ((np.exp(-u*(((k+1)*s)-(k*s))))*(fh(h))*(fx(x)))
            
                #CASO 11
                if W == k and k >= 1 and k < M:
                    d11,_=dblquad(fd11, (k-1)*s, (k)*s, lambda x: 0, lambda x: (k)*s-x)
                    pt11,_=dblquad(fpt11, (k-1)*s, (k)*s, lambda x: 0, lambda x: (k)*s-x)
                            
                    c11=pt11*(p)*((ci*(k)+cf))
                    t11=pt11*(p)*(k+1)*s
                    d11=d11*(p)
                    pt11=pt11*(p)
                            
                    cust11 = cust11 + c11
                    tam11 = tam11 + t11
                    down11 = down11 + d11
                    probt11 = probt11 + pt11
                            
                    sc = sc + c11
                    sv = sv + t11
                    dt = dt + d11
                    pt = pt + pt11
            
                ###############################################CASO 12
                def fd12(h,x): #Caso 12
                    return ((((i*s)-(x+h)))*(np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt12(h,x): #Caso 12
                    return ((np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 12
                if k >= 1:
                    for i in range(W+1, M+1):
                        d12,_=dblquad(fd12, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                        pt12,_=dblquad(fpt12, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                            
                        c12=pt12*(p)*((ci*(k)+cf))
                        t12=pt12*(p)*(i*s)
                        d12=d12*(p)
                        pt12=pt12*(p)
                        
                        cust12 = cust12 + c12
                        tam12 = tam12 + t12
                        down12 = down12 + d12
                        probt12 = probt12 + pt12
                        
                        sc = sc + c12
                        sv = sv + t12
                        dt = dt + d12
                        pt = pt + pt12
            
                ###############################################CASO 13
                def fd13(h,x): #Caso 13
                    return ((((i*s)-(x+h)))*(np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt13(h,x): #Caso 13
                    return ((np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 13
                if W >= k+2:
                    lim = W+1
                else:
                    lim = k+2
                
                for i in range(lim, M):
                    for j in range(k+1, i):
                        d13,_=dblquad(fd13, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                        pt13,_=dblquad(fpt13, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x)
                            
                        c13=pt13*(1-p)*((ci*(k)+cf))
                        t13=pt13*(1-p)*((i*s))
                        d13=d13*(1-p)
                        pt13=pt13*(1-p)
                            
                        cust13 = cust13 + c13
                        tam13 = tam13 + t13
                        down13 = down13 + d13        
                        probt13 = probt13 + pt13
                        
                        sc = sc + c13
                        sv = sv + t13
                        dt = dt + d13
                        pt = pt + pt13
            
                ###############################################CASO 14
                def fd14(h,x): #Caso 14
                    return ((((i*s)-(x+h)))*(np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt14(h,x): #Caso 14
                    return ((np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 14
                if W >= k+3:
                    lim = W+1
                else:
                    lim = k+3
                    
                for i in range(lim, M+1):
                    for j in range(k+1, i-1):
                        d14,_=dblquad(fd14, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x)
                        pt14,_=dblquad(fpt14, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x)
                        
                        c14=pt14*(p)*((ci*(k)+cf))
                        t14=pt14*(p)*((i*s))
                        d14=d14*(p)
                        pt14=pt14*(p)
                        
                        cust14 = cust14 + c14
                        tam14 = tam14 + t14
                        down14 = down14 + d14        
                        probt14 = probt14 + pt14
                        
                        sc = sc + c14
                        sv = sv + t14
                        dt = dt + d14
                        pt = pt + pt14
            
                ###############################################CASO 15
                def fd15(h,x): #Caso 15
                    return ((((M*s)-(x+h)))*(np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt15(h,x): #Caso 15
                    return ((np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 15
                for j in range(k+1, M):
                    d15,_=dblquad(fd15, (j-1)*s, j*s, lambda x: (M-1)*s-x, lambda x: M*s-x)
                    pt15,_=dblquad(fpt15, (j-1)*s, j*s, lambda x: (M-1)*s-x, lambda x: M*s-x)
                    
                    c15=pt15*((ci*(k)+cf))
                    t15=pt15*((M*s))
                    d15=d15
                    pt15=pt15
                    
                    cust15 = cust15 + c15
                    tam15 = tam15 + t15
                    down15 = down15 + d15           
                    probt15 = probt15 + pt15
                
                    sc = sc + c15
                    sv = sv + t15
                    dt = dt + d15
                    pt = pt + pt15
            
                ###############################################CASO 16
                def fd16(h,x): #Caso 16
                    return ((((i*s)-(x+h)))*(np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt16(h,x): #Caso 16
                    return ((np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 16
                for i in range(W+1, M):
                    d16,_=dblquad(fd16, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                    pt16,_=dblquad(fpt16, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x)
                    
                    c16=pt16*(1-p)*((ci*(k)+cf))
                    t16=pt16*(1-p)*((i*s))
                    d16=d16*(1-p)
                    pt16=pt16*(1-p)
                    
                    cust16 = cust16 + c16
                    tam16 = tam16 + t16
                    down16 = down16 + d16           
                    probt16 = probt16 + pt16
                    
                    sc = sc + c16
                    sv = sv + t16
                    dt = dt + d16
                    pt = pt + pt16
            
                ###############################################CASO 17
                def fd17(h,x): #Caso 17
                    return ((((i*s)-(x+h)))*(np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt17(h,x): #Caso 17
                    return ((np.exp(-u*((i*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 17
                if W >= k+2:
                    lim = W+1
                else:
                    lim = k+2
                
                for i in range(lim, M+1):
                    d17,_=dblquad(fd17, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                    pt17,_=dblquad(fpt17, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x)
                        
                    c17=pt17*(p)*((ci*(k)+cf))
                    t17=pt17*(p)*((i*s))
                    d17=d17*(p)
                    pt17=pt17*(p)
                        
                    cust17 = cust17 + c17
                    tam17 = tam17 + t17
                    down17 = down17 + d17     
                    probt17 = probt17 + pt17
                        
                    sc = sc + c17
                    sv = sv + t17
                    dt = dt + d17
                    pt = pt + pt17
            
                ###############################################CASO 18
                def fd18(h,x): #Caso 18
                    return ((((M*s)-(x+h)))*(np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
                def fpt18(h,x): #Caso 18
                    return ((np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 18
                if k < M:
                    d18,_=dblquad(fd18, (M-1)*s, M*s, lambda x: 0, lambda x: M*s-x)
                    pt18,_=dblquad(fpt18, (M-1)*s, M*s, lambda x: 0, lambda x: M*s-x)
                    
                    c18=pt18*((ci*(k)+cf))
                    t18=pt18*((M*s))
                    d18=d18
                    pt18=pt18
                
                    cust18 = cust18 + c18
                    tam18 =   tam18 + t18
                    down18 = down18 + d18 
                    probt18 = probt18 + pt18
                    
                    sc = sc + c18
                    sv = sv + t18
                    dt = dt + d18
                    pt = pt + pt18
                
                ###############################################CASO 19
                def fpt19(h,x): #Caso 19
                    return ((np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 19
                if k >= 1 and k < M:
                    pt19,_=dblquad(fpt19, (k-1)*s, k*s, lambda x: M*s-x, lambda x: np.inf)
                    
                    c19=pt19*(p)*((ci*(k)+cp))
                    t19=pt19*(p)*((M*s))
                    pt19=pt19*(p)
                    
                    cust19 = cust19 + c19
                    tam19 = tam19 + t19
                    probt19 = probt19 + pt19
                    
                    sc = sc + c19
                    sv = sv + t19
                    pt = pt + pt19
            
                ###############################################CASO 20
                def fpt20(h,x): #Caso 20
                    return ((np.exp(-u*((M*s)-(W*s))))*(fh(h))*(fx(x)))
            
                #CASO 20
                for j in range(k+1, M+1):
                    pt20,_=dblquad(fpt20, (j-1)*s, j*s, lambda x: M*s-x, lambda x: np.inf)
                    
                    c20=pt20*((ci*(k)+cp))
                    t20=pt20*((M*s))
                    pt20=pt20
                    
                    cust20 = cust20 + c20
                    tam20 = tam20 + t20
                    probt20 = probt20 + pt20
                    
                    sc = sc + c20
                    sv = sv + t20
                    pt = pt + pt20
            
                ###############################################CASO 21
                #CASO 21
                r21,_=quad(fx, M*s, np.inf)
                
                c21 = (k*ci+cp)*(r21)*(np.exp(-u*(M*s-W*s)))
                t21 = (M*s)*(r21)*(np.exp(-u*(M*s-W*s)))
                pt21 = (r21)*(np.exp(-u*(M*s-W*s)))
                
                cust21 = cust21 + c21
                tam21 = tam21 + t21
                probt21 = probt21 + pt21
                
                sc = sc + c21
                sv = sv + t21
                pt = pt + pt21
                
                ###############################################CASO 22
                def ft22(z,h,x):
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt22(z,h,x):
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 22
                if k >= 1:
                    for i in range(W+1, M+1):
                        t22,_=tplquad(ft22, (k-1)*s, (k)*s, lambda x: (i-1)*s-x, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                        pt22,_=tplquad(fpt22, (k-1)*s, (k)*s, lambda x: (i-1)*s-x, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    
                        c22=pt22*(p)*(k*ci+co)
                        t22=t22*(p)
                        pt22=pt22*(p)
                    
                        cust22 = cust22 + c22
                        tam22 = tam22 + t22
                        probt22 = probt22 + pt22
            
                        sc = sc + c22
                        sv = sv + t22
                        pt = pt + pt22
            
                ###############################################CASO 23
                def ft23(z,h,x): #Caso 23
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt23(z,h,x): #Caso 23
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 23
                if W <= M-2:
                    if W == k:
                        lim = k+2
                    else:
                        lim = W+1
            
                    for i in range(lim, M):
                        for j in range(k+1, i):
                            t23,_=tplquad(ft23, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                            pt23,_=tplquad(fpt23, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                            
                            c23=pt23*(1-p)*(k*ci+co)
                            t23=t23*(1-p)
                            pt23=pt23*(1-p)
                            
                            cust23 = cust23 + c23
                            tam23 = tam23 + t23
                            probt23 = probt23 + pt23
            
                            sc = sc + c23
                            sv = sv + t23
                            pt = pt + pt23
                
                ###############################################CASO 24   
                def ft24(z,h,x): #Caso 24
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt24(z,h,x): #Caso 24
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 24
                if W == k:
                    lim = k+3
                else:
                    lim = W+2
            
                for i in range(lim, M+1):
                    for j in range(k+1, i-1):
                        t24,_=tplquad(ft24, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                        pt24,_=tplquad(fpt24, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                            
                        c24=pt24*(p)*(k*ci+co)
                        t24=t24*(p)
                        pt24=pt24*(p)
                        
                        cust24 = cust24 + c24
                        tam24 = tam24 + t24
                        probt24 = probt24 + pt24
                        
                        sc = sc + c24
                        sv = sv + t24
                        pt = pt + pt24
            
                ###############################################CASO 25
                def ft25(z,h,x): #Caso 25
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt25(z,h,x): #Caso 25
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 25
                if W < M:
                    for j in range(k+1, M):
                        t25,_=tplquad(ft25, (j-1)*s, j*s, lambda x: (M-1)*s-x, lambda x: M*s-x, lambda x, h: W*s, lambda x, h: x+h)
                        pt25,_=tplquad(fpt25, (j-1)*s, j*s, lambda x: (M-1)*s-x, lambda x: M*s-x, lambda x, h: W*s, lambda x, h: x+h)
                        
                        c25=pt25*(k*ci+co)
                        t25=t25
                        pt25=pt25
                        
                        cust25 = cust25 + c25
                        tam25 = tam25 + t25
                        probt25 = probt25 + pt25
                        
                        sc = sc + c25
                        sv = sv + t25
                        pt = pt + pt25
                        
                ###############################################CASO 26
                def ft26(z,h,x): #Caso 26
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt26(z,h,x): #Caso 26
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 26
                for i in range(W+1, M):
                    t26,_=tplquad(ft26, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    pt26,_=tplquad(fpt26, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    
                    c26=pt26*(1-p)*(k*ci+co)
                    t26=t26*(1-p)
                    pt26=pt26*(1-p)
                    
                    cust26 = cust26 + c26
                    tam26 = tam26 + t26
                    probt26 = probt26 + pt26
                    
                    sc = sc + c26
                    sv = sv + t26
                    pt = pt + pt26
            
                ###############################################CASO 27
                def ft27(z,h,x): #Caso 27
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt27(z,h,x): #Caso 27
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 27
                for i in range(W+2, M+1):
                    t27,_=tplquad(ft27, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    pt27,_=tplquad(fpt27, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    
                    c27=pt27*(p)*(k*ci+co)
                    t27=t27*(p)
                    pt27=pt27*(p)
            
                    cust27 = cust27 + c27
                    tam27 = tam27 + t27
                    probt27 = probt27 + pt27
                    
                    sc = sc + c27
                    sv = sv + t27
                    pt = pt + pt27
            
                ###############################################CASO 28
                def ft28(z,h,x): #Caso 28
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt28(z,h,x): #Caso 28
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 28
                if W < M:
                    t28,_=tplquad(ft28, (M-1)*s, (M)*s, lambda x: 0, lambda x: (M)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    pt28,_=tplquad(fpt28, (M-1)*s, (M)*s, lambda x: 0, lambda x: (M)*s-x, lambda x, h: W*s, lambda x, h: x+h)
                    
                    c28=pt28*(k*ci+co)
                    t28=t28
                    pt28=pt28
                    
                    cust28 = cust28 + c28
                    tam28 = tam28 + t28
                    probt28 = probt28 + pt28
                    
                    sc = sc + c28
                    sv = sv + t28
                    pt = pt + pt28
               
                ###############################################CASO 29
                def ft29(z,h,x): #Caso 29
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt29(z,h,x): #Caso 29
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 29
                if k > 0:
                    t29,_=tplquad(ft29, (k-1)*s, k*s, lambda x: (M)*s-x, lambda x: np.inf, lambda x, h: W*s, lambda x, h: M*s)
                    pt29,_=tplquad(fpt29, (k-1)*s, k*s, lambda x: (M)*s-x, lambda x: np.inf, lambda x, h: W*s, lambda x, h: M*s)
                                
                    c29=pt29*(p)*(k*ci+co)
                    t29=t29*(p)
                    pt29=pt29*(p)
                            
                    cust29 = cust29 + c29
                    tam29 = tam29 + t29
                    probt29 = probt29 + pt29
                            
                    sc = sc + c29
                    sv = sv + t29
                    pt = pt + pt29
            
                ###############################################CASO 30
                def ft30(z,h,x): #Caso 30
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt30(z,h,x): #Caso 30
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 30
                for j in range(k+1, M+1):
                    t30,_=tplquad(ft30, (j-1)*s, (j)*s, lambda x: M*s-x, lambda x: np.inf, lambda x, h: W*s, lambda x, h: M*s)
                    pt30,_=tplquad(fpt30, (j-1)*s, (j)*s, lambda x: M*s-x, lambda x: np.inf, lambda x, h: W*s, lambda x, h: M*s)
                    
                    c30=pt30*(k*ci+co)
                    t30=t30
                    pt30=pt30
                    
                    cust30 = cust30 + c30
                    tam30  =  tam30 + t30
                    probt30 = probt30 + pt30
                
                    sc = sc + c30
                    sv = sv + t30
                    pt = pt + pt30
            
                ###############################################CASO 31
                def ft31(z, x): #Caso 31
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fx(x)))
                def fpt31(z, x): #Caso 31
                    return ((u)*(np.exp(-u*(z-W*s)))*(fx(x)))
            
                #CASO 31
                t31,_=dblquad(ft31, (M)*s, np.inf, lambda x: W*s, lambda x: M*s)
                pt31,_=dblquad(fpt31, (M)*s, np.inf, lambda x: W*s, lambda x: M*s)
                    
                c31=pt31*(k*ci+co)
                t31=t31
                pt31=pt31
                
                cust31 = cust31 + c31
                tam31  =  tam31 + t31
                probt31 = probt31 + pt31
            
                sc = sc + c31
                sv = sv + t31
                pt = pt + pt31
            
                ###############################################CASO 32
                def ft32(z,h,x): #Caso 32
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd32(z,h,x): #Caso 32
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt32(z,h,x): #Caso 32
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 32
                if W == k and k >= 1:
                    t32,_=tplquad(ft32, (k-1)*s, (k)*s, lambda x: 0, lambda x: (k)*s-x, lambda x, h: (k)*s, lambda x, h: (k+1)*s)
                    d32,_=tplquad(fd32, (k-1)*s, (k)*s, lambda x: 0, lambda x: (k)*s-x, lambda x, h: (k)*s, lambda x, h: (k+1)*s)
                    pt32,_=tplquad(fpt32, (k-1)*s, (k)*s, lambda x: 0, lambda x: (k)*s-x, lambda x, h: (k)*s, lambda x, h: (k+1)*s)
                    
                    c32=pt32*(p)*((i-1)*ci+co)
                    t32=t32*(p)
                    d32=d32*(p)
                    pt32=pt32*(p)
                    
                    cust32 = cust32 + c32
                    tam32  = tam32 + t32
                    down32 = down32 + d32  
                    probt32 = probt32 + pt32         
                       
                    sc = sc + c32
                    sv = sv + t32
                    dt = dt + d32
                    pt = pt + pt32
            
                ###############################################CASO 33
                def ft33(z,h,x): #Caso 33
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd33(z,h,x): #Caso 33
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt33(z,h,x): #Caso 33
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 33
                if k >= 1:
                    for i in range(W+1, M+1):
                        t33,_=tplquad(ft33, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        d33,_=tplquad(fd33, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        pt33,_=tplquad(fpt33, (k-1)*s, k*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                            
                        c33=pt33*(p)*(k*ci+co)
                        t33=t33*(p)
                        d33=d33*(p)
                        pt33=pt33*(p)
                        
                        cust33 = cust33 + c33
                        tam33  = tam33 + t33
                        down33 = down33 + d33     
                        probt33 = probt33 + pt33      
                               
                        sc = sc + c33
                        sv = sv + t33
                        dt = dt + d33 
                        pt = pt + pt33
            
                ###############################################CASO 34
                def ft34(z,h,x): #Caso 34
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd34(z,h,x): #Caso 34
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt34(z,h,x): #Caso 34
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 34
                if W == k:
                    lim = k+2
                else:
                    lim = W+1
            
                for i in range(lim, M):
                    for j in range(k+1, i):
                        t34,_=tplquad(ft34, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        d34,_=tplquad(fd34, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        pt34,_=tplquad(fpt34, (j-1)*s, j*s, lambda x: (i-1)*s-x, lambda x: (i)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        
                        c34=pt34*(1-p)*(k*ci+co)
                        t34=t34*(1-p)
                        d34=d34*(1-p)
                        pt34=pt34*(1-p)
                            
                        cust34 = cust34 + c34
                        tam34  = tam34 + t34
                        down34 = down34 + d34      
                        probt34 = probt34 + pt34
                            
                        sc = sc + c34
                        sv = sv + t34
                        dt = dt + d34
                        pt = pt + pt34
            
                ###############################################CASO 35
                def ft35(z,h,x): #Caso 35
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd35(z,h,x): #Caso 35
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt35(z,h,x): #Caso 35
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 35
                if W == k:
                    lim = k+3
                else:
                    lim = W+2
                
                for i in range(W+2, M+1):
                    for j in range(k+1, i-1):
                        t35,_=tplquad(ft35, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        d35,_=tplquad(fd35, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        pt35,_=tplquad(fpt35, (j-1)*s, j*s, lambda x: (i-2)*s-x, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                        
                        c35=pt35*(p)*(k*ci+co)
                        t35=t35*(p)
                        d35=d35*(p)
                        pt35=pt35*(p)
                            
                        cust35 = cust35 + c35
                        tam35  = tam35 + t35
                        down35 = down35 + d35  
                        probt35 = probt35 + pt35         
                        
                        sc = sc + c35
                        sv = sv + t35
                        dt = dt + d35
                        pt = pt + pt35
            
                ###############################################CASO 36
                def ft36(z,h,x): #Caso 36
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd36(z,h,x): #Caso 36
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt36(z,h,x): #Caso 36
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 36
                if W <= M-1:
                    for j in range(k+1, W):
                        t36,_=tplquad(ft36, (j-1)*s, (j)*s, lambda x: (W-1)*s-x, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                        d36,_=tplquad(fd36, (j-1)*s, (j)*s, lambda x: (W-1)*s-x, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                        pt36,_=tplquad(fpt36, (j-1)*s, (j)*s, lambda x: (W-1)*s-x, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                        
                        c36=pt36*(p)*(k*ci+co)
                        t36=t36*(p)
                        d36=d36*(p)
                        pt36=pt36*(p)
                        
                        cust36 = cust36 + c36
                        tam36  = tam36 + t36
                        down36 = down36 + d36     
                        probt36 = probt36 + pt36
                        
                        sc = sc + c36
                        sv = sv + t36
                        dt = dt + d36
                        pt = pt + pt36
            
                ###############################################CASO 37
                def ft37(z,h,x): #Caso 37
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd37(z,h,x): #Caso 37
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt37(z,h,x): #Caso 37
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 37
                if W <= M-1:
                    for j in range(k+1, M):
                        t37,_=tplquad(ft37, (j-1)*s, (j)*s, lambda x: (M-1)*s-x, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: (M)*s)
                        d37,_=tplquad(fd37, (j-1)*s, (j)*s, lambda x: (M-1)*s-x, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: (M)*s)
                        pt37,_=tplquad(fpt37, (j-1)*s, (j)*s, lambda x: (M-1)*s-x, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: (M)*s)
                        
                        c37=pt37*(k*ci+co)
                        t37=t37
                        d37=d37
                        pt37=pt37
                        
                        cust37 = cust37 + c37
                        tam37  = tam37 + t37
                        down37 = down37 + d37   
                        probt37 = probt37 + pt37        
                        
                        sc = sc + c37
                        sv = sv + t37
                        dt = dt + d37
                        pt = pt + pt37 
            
                ###############################################CASO 38
                def ft38(z,h,x): #Caso 38
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd38(z,h,x): #Caso 38
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt38(z,h,x): #Caso 38
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 38
                for i in range(W+1, M):
                    t38,_=tplquad(ft38, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    d38,_=tplquad(fd38, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    pt38,_=tplquad(fpt38, (i-1)*s, i*s, lambda x: 0, lambda x: i*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    
                    c38=pt38*(1-p)*(k*ci+co)
                    t38=t38*(1-p)
                    d38=d38*(1-p)
                    pt38=pt38*(1-p)
                            
                    cust38 = cust38 + c38
                    tam38  = tam38 + t38
                    down38 = down38 + d38    
                    probt38 = probt38 + pt38       
                    
                    sc = sc + c38
                    sv = sv + t38
                    dt = dt + d38
                    pt = pt + pt38
            
                ###############################################CASO 39
                def ft39(z,h,x): #Caso 39
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd39(z,h,x): #Caso 39
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt39(z,h,x): #Caso 39
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 39
                for i in range(W+2, M+1):
                    t39,_=tplquad(ft39, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    d39,_=tplquad(fd39, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    pt39,_=tplquad(fpt39, (i-2)*s, (i-1)*s, lambda x: 0, lambda x: (i-1)*s-x, lambda x, h: x+h, lambda x, h: i*s)
                    
                    c39=pt39*(p)*(k*ci+co)
                    t39=t39*(p)
                    d39=d39*(p)
                    pt39=pt39*(p)
            
                    cust39 = cust39 + c39
                    tam39  = tam39 + t39
                    down39 = down39 + d39   
                    probt39 = probt39 + pt39        
            
                    sc = sc + c39
                    sv = sv + t39
                    dt = dt + d39
                    pt = pt + pt39
            
                ###############################################CASO 40
                def ft40(z,h,x): #Caso 40
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd40(z,h,x): #Caso 40
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt40(z,h,x): #Caso 40
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                
                #CASO 40
                if W > k and W <= M-1:
                    t40,_=tplquad(ft40, (W-1)*s, (W)*s, lambda x: 0, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                    d40,_=tplquad(fd40, (W-1)*s, (W)*s, lambda x: 0, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                    pt40,_=tplquad(fpt40, (W-1)*s, (W)*s, lambda x: 0, lambda x: (W)*s-x, lambda x, h: W*s, lambda x, h: (W+1)*s)
                    
                    c40=pt40*(p)*(k*ci+co)
                    t40=t40*(p)
                    d40=d40*(p)
                    pt40=pt40*(p)
            
                    cust40 = cust40 + c40
                    tam40  = tam40 + t40
                    down40 = down40 + d40     
                    probt40 = probt40 + pt40      
                
                    sc = sc + c40
                    sv = sv + t40
                    dt = dt + d40
                    pt = pt + pt40
            
                ###############################################CASO 41
                def ft41(z,h,x): #Caso 41
                    return ((z)*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fd41(z,h,x): #Caso 41
                    return ((z-(x+h))*(u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
                def fpt41(z,h,x): #Caso 41
                    return ((u)*(np.exp(-u*(z-W*s)))*(fh(h))*(fx(x)))
            
                #CASO 41
                if W <= M-1:
                    t41,_=tplquad(ft41, (M-1)*s, (M)*s, lambda x: 0, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: M*s)
                    d41,_=tplquad(fd41, (M-1)*s, (M)*s, lambda x: 0, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: M*s)
                    pt41,_=tplquad(fpt41, (M-1)*s, (M)*s, lambda x: 0, lambda x: (M)*s-x, lambda x, h: x+h, lambda x, h: M*s)
                    
                    c41=pt41*(k*ci+co)
                    t41=t41
                    d41=d41
                    pt41=pt41
                    
                    cust41 = cust41 + c41
                    tam41  = tam41 + t41
                    down41 = down41 + d41   
                    probt41 = probt41 + pt41        
                    
                    sc = sc + c41
                    sv = sv + t41
                    dt = dt + d41
                    pt = pt + pt41
            
            
                #Expected cost
                sc = sc + dt*cd
            
                #Expected length
                sv = sv
            
                #Expected cost-rate
                c = sc/sv
                
                dr = dt/sv

                #MTBOF
                probfalha = probt1 + probt2 + probt3 + probt4 + probt5 + probt6 + probt7 + probt8 + probt11 + probt12 + probt13 + probt14 + probt15 + probt16 + probt17 + probt18 + probt32 + probt33 + probt34 + probt35 + probt36 + probt37 + probt38 + probt39 + probt40 + probt41
                mtbof_ = sv/probfalha
                
                return c, dr, mtbof_
                
            c, dr, mtbof_ = otm(k, W, M)
            st.write("Taxa de custo: {:.3f}" .format(c))
            st.write("Taxa de inatividade: {:.3f}" .format(dr))
            st.write("Tempo médio entre falhas operacionais: {:.3f}" .format(mtbof_))
main()
