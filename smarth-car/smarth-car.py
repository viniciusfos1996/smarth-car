#SENSOR_INFRAVERMELHO
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
# coding:utf-8
 
import sys
import time
import signal
import RPi.GPIO as GPIO
 
# Define a numeração dos pinos de acordo com a placa
GPIO.setmode(GPIO.BOARD)
 
# Função para finalizar o acesso à GPIO do Raspberry de forma segura
def clean():
    GPIO.cleanup()
 
# Função para finalizar o programa de forma segura com CTRL-C
def sigint_handler(signum, instant):
    clean()
    sys.exit()
 
# Ativar a captura do sinal SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, sigint_handler)
 
# TRIG será conectado ao pino 18. ECHO ao pino 16.
TRIG = 18
ECHO = 16
 
# Variáveis para auxiliar no controle do loop principal
# sampling_rate: taxa de amostragem em Hz, isto é, em média,
#   quantas leituras do sonar serão feitas por segundo
# speed_of_sound: velocidade do som no ar a 30ºC em m/s
# max_distance: máxima distância permitida para medição
# max_delta_t: um valor máximo para a variável delta_t,
#   baseado na distância máxima max_distance
sampling_rate = 20.0
speed_of_sound = 349.10
max_distance = 4.0
max_delta_t = max_distance / speed_of_sound
 
# Define TRIG como saída digital
# Define ECHO como entrada digital
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
# Inicializa TRIG em nível lógico baixo
GPIO.output(TRIG, False)
time.sleep(1)
 
print ("Sampling Rate:", sampling_rate, "Hz")
print ("Distances (cm)")
 
# Loop principal. Será executado até que que seja pressionado CTRL-C
while True:
 
    # Gera um pulso de 10ms em TRIG.
    # Essa ação vai resultar na transmissão de ondas ultrassônicas pelo
    # transmissor do módulo sonar.
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
 
    # Atualiza a variável start_t enquanto ECHO está em nível lógico baixo.
    # Quando ECHO trocar de estado, start_t manterá seu valor, marcando
    # o momento da borda de subida de ECHO. Este é o momento em que as ondas
    # sonoras acabaram de ser enviadas pelo transmissor.
    while GPIO.input(ECHO) == 0:
      start_t = time.time()
 
    # Atualiza a variável end_t enquando ECHO está em alto. Quando ECHO
    # voltar ao nível baixo, end_t vai manter seu valor, marcando o tempo
    # da borda de descida de ECHO, ou o momento em que as ondas refletidas
    # por um objeto foram captadas pelo receptor. Caso o intervalo de tempo
    # seja maior que max_delta_t, o loop de espera também será interrompido.
    while GPIO.input(ECHO) == 1 and time.time() - start_t < max_delta_t:
      end_t = time.time()
 
    # Se a diferença entre end_t e start_t estiver dentro dos limites impostos,
    # atualizamos a variável delta_t e calculamos a distância até um obstáculo.
    # Caso o valor de delta_t não esteja nos limites determinados definimos a
    # distância como -1, sinalizando uma medida mal-sucedida.
    if end_t - start_t < max_delta_t:
        delta_t = end_t - start_t
        distance = 100*(0.5 * delta_t * speed_of_sound)
    else:
        distance = -1
 
    # Imprime o valor da distância arredondado para duas casas decimais
    print (round(distance, 2))
 
    # Um pequeno delay para manter a média da taxa de amostragem
    time.sleep(1/sampling_rate)
