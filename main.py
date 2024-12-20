import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import quad #Single integral
from PIL import Image

def main():
    #criando 3 colunas
    col1, col2, col3= st.columns(3)
    foto = Image.open('randomen.png')
    #st.sidebar.image("randomen.png", use_column_width=True)
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    #O código abaixo insere o título, mas não centraliza.
    #st.title('KMT Policy Software')
    #O código abaixo centraliza e atribui cor
    st.markdown("<h2 style='text-align: center; color: #306754;'>Política O&M Orientada por Mineração de Padrões Sequenciais</h2>", unsafe_allow_html=True)
    
    menu = ["Aplicativo", "Informações", "Website"]
    
    choice = st.sidebar.selectbox("Selecione aqui", menu)
    
    if choice == menu[0]:
        st.header(menu[0])
        st.subheader("Insira os parâmetros abaixo:")

        a1=st.number_input("Insira a vida característica do componente fraco", min_value = 0.0, value = 0.40) #escala fraca
        b1=st.number_input("Insira o parâmetro de forma do componente fraco", min_value = 0.0, value = 2.50) #forma fraca
        a2=st.number_input("Insira a vida característica do componente forte", min_value = 0.0, value = 1.80) #escala forte.
        b2=st.number_input("Insira o parâmetro de forma do componente forte", min_value = 0.0, value = 5.00) #forma forte
        p =0.10 #parâmetro de mistura
        l =1.00 #inverso da média da distribuição do delay time
        u =1.00 #taxa de chegada de oportunidades
        ci=0.05 #custo de inspeção
        cd=0.60 #custo de substituição preventiva numa inspeção
        co=0.70 #custo da preventiva na oportunidade
        cr=1.00 #custo da preventiva
        cf=5.00 #custo de falha
        c =5.00 #custo de estado defeituoso 
        
        eta=st.number_input("Insert the characteristic life of the component (𝜂)", min_value = 0.0, value = 25.0)
        beta=st.number_input("Insert the shape parameter of the component (𝛽)", min_value = 0.0, value = 3.0) 
        q=st.number_input("Insert the probability for replacement by opportunity (q)", min_value = 0.0, max_value=1.0, value = 0.4) 
        s=st.number_input("Insert the Insert the time between slots (s)", min_value = 0.001, value = 1.0) 
        taxa_lambda=st.number_input("Insert the rate of demands (\u03BB)", min_value = 0.0, value = 0.01) 
        CO = st.number_input("Insert the cost of a replacement by opportunity (cO)", min_value=0.0, value=0.5)
        CM = st.number_input("Insert the cost of a schedule preventive replacement (cM)", min_value=0.0, value=1.0)
        CF=st.number_input("Insert the cost of a corrective replacement (cF)", min_value = 0.0, value = 2.0)
        C_d=st.number_input("Insert the cost of an unmet demand (cd)", min_value = 0.0, value = 20000.0) 

        st.subheader("Click on botton below to run this application:")    
        botao = st.button("Get cost-rate")        
        if botao:
            CD=C_d*taxa_lambda 

            def fx(x):#weibull densidade (componente fraco)
                return (beta/eta)*((x/eta)**(beta-1))*np.exp(-(x/eta)**beta)
            def Fx(x):
                return (1-np.exp(-(x/eta)**beta))
            def Rx(x):
                return 1-Fx(x)

            def otm(W,M):
                def CASO1(W,M):
                    P1=0
                    L1=0
                    C1=0
                    D1=0
                    if W>0:
                        for i in range(1,W):
                            P1=P1+(quad(lambda x: fx(x),(i-1)*s,i*s)[0])
                            L1=L1+((i*s)*(quad(lambda x: fx(x),(i-1)*s,i*s)[0]))
                            D1=D1+(quad(lambda x: ((i*s)-x)*fx(x),(i-1)*s,i*s)[0])
                        C1=C1+(CF*P1)
                    return P1, L1, D1, C1
                def CASO2(W,M):
                    P2=0
                    L2=0
                    D2=0
                    C2=0
                    if W!=0:
                        for i in range(W,M):
                            P2=P2+(((1-q)**(i-W))*(quad(lambda x: fx(x),(i-1)*s,i*s)[0]))
                            L2=L2+((i*s)*(((1-q)**(i-W))*(quad(lambda x: fx(x),(i-1)*s,i*s)[0])))
                            D2=D2+(((1-q)**(i-W))*(quad(lambda x: ((i*s)-x)*fx(x),(i-1)*s,i*s)[0]))
                        C2=C2+(CF*P2)
                    elif W==0:
                        for i in range(1,M):
                            P2=P2+(((1-q)**(i-1))*(quad(lambda x: fx(x),(i-1)*s,i*s)[0]))
                            L2=L2+((i*s)*(((1-q)**(i-1))*(quad(lambda x: fx(x),(i-1)*s,i*s)[0])))
                            D2=D2+(((1-q)**(i-1))*(quad(lambda x: ((i*s)-x)*fx(x),(i-1)*s,i*s)[0]))
                        C2=C2+(CF*P2)
                    return P2, L2, D2, C2
                def CASO3(W,M):
                    P3=0
                    L3=0
                    C3=0
                    if W!=0:
                        for i in range(W,M):
                            P3=P3+(Rx(i*s)*q*((1-q)**(i-W)))
                            L3=L3+((i*s)*(Rx(i*s)*q*((1-q)**(i-W))))
                        C3=C3+(CO*P3)
                    elif W==0:
                        for i in range(1,M):
                            P3=P3+(Rx(i*s)*q*((1-q)**(i-1)))
                            L3=L3+((i*s)*(Rx(i*s)*q*((1-q)**(i-1))))
                        C3=C3+(CO*P3)      
                    return P3, L3, C3
                def CASO4(W,M):
                    if W!=0:
                        P4=((1-q)**(M-W))*(quad(lambda x: fx(x),(M-1)*s,M*s)[0])
                        L4=(M*s)*P4
                        D4=((1-q)**(M-W))*(quad(lambda x: ((M*s)-x)*fx(x),(M-1)*s,M*s)[0])
                        C4=(CM*P4)
                    elif W==0:
                        P4=((1-q)**(M-1))*(quad(lambda x: fx(x),(M-1)*s,M*s)[0])
                        L4=(M*s)*P4
                        D4=((1-q)**(M-1))*(quad(lambda x: ((M*s)-x)*fx(x),(M-1)*s,M*s)[0])
                        C4=(CM*P4)
                    return P4, L4, D4, C4
                def CASO5(W,M):
                    if W!=0:
                        P5=((1-q)**(M-W))*Rx(M*s)
                        L5=(M*s)*P5
                        C5=(CM*P5)
                    if W==0:
                        P5=((1-q)**(M-1))*Rx(M*s)
                        L5=(M*s)*P5
                        C5=(CM*P5)
                    return P5, L5, C5

                CASO1=CASO1(W,M)
                CASO2=CASO2(W,M)
                CASO3=CASO3(W,M)
                CASO4=CASO4(W,M)
                CASO5=CASO5(W,M)

                PROB_TOTAL=CASO1[0]+CASO2[0]+CASO3[0]+CASO4[0]+CASO5[0]
                UNAVAILABILITY=(CASO1[2]+CASO2[2]+CASO4[2])/(CASO1[1]+CASO2[1]+CASO3[1]+CASO4[1]+CASO5[1])
                COST_RATE=((CASO1[3]+CASO2[3]+CASO3[2]+CASO4[3]+CASO5[2])+(CD*(CASO1[2]+CASO2[2]+CASO4[2])))/(CASO1[1]+CASO2[1]+CASO3[1]+CASO4[1]+CASO5[1])
                MTBOF=(CASO1[1]+CASO2[1]+CASO3[1]+CASO4[1]+CASO5[1])/(CASO1[0]+CASO2[0]+CASO4[0])
                
                return COST_RATE, UNAVAILABILITY, MTBOF, PROB_TOTAL
            Resultado_CR=1000000000000000
            for W in range(0,int(round(eta))+5):
                for M in range(W,int(round(eta))+5):
                    #print("W: "+str(W)+"; M: "+str(M))
                    resultado=otm(W,M)
                    if resultado[0]<=Resultado_CR:
                        Resultado_CR=resultado[0]
                        Resultado_Una=resultado[1]
                        Resultado_MTBOF=resultado[2]
                        Resultado_W=W
                        Resultado_M=M
            ####################### EXECUTA OTIMIZADOR#$#################################
            st.write("---RESULTS---")
            st.markdown("*W\\*:* {:d}".format(Resultado_W))
            st.markdown("*M\\*:* {:d}".format(Resultado_M))
            st.write("COST-RATE: {:.3f}".format(round(Resultado_CR, 3)))
            st.write("AVARAGE UNAVAILABILITY: {:.3f}".format(round(Resultado_Una, 3)))
            st.write("MTBOF: {:.2f}".format(round(Resultado_MTBOF, 2)))
            
    if choice == menu[1]:
        st.header(menu[1])
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>This prototype was created by members of the RANDOM research group, which aims to assist in the application of the {W, M} policy developed in the paper 'On periodic maintenance for a protection system'.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>This prototype has restrictions regarding the solution search space. If it is in the user's interest to use a wider range of solution combinations or if there is any question about the study and/or this prototype can be directed to any of the email addresses below. Also, this application is still in the development stage. Finally, if this application is used for any purpose, all authors should be informed.</h6>", unsafe_allow_html=True)
        
        st.write('''

a.j.s.rodrigues@random.org.br

c.a.v.cavalcante@random.org.br

''' .format(chr(948), chr(948), chr(948), chr(948), chr(948)))       
    if choice==menu[2]:
        st.header(menu[2])
        
        st.write('''The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 
                 in order to bring together different researchers who work in the following areas: risk, maintenance a
                 nd operation modelling. Learn more about it through our website.''')
        st.markdown('[Click here to be redirected to our website](http://random.org.br/en/)',False)        
if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())



