# Neurociencia

### Nota para correr el experimento

El programa se ejecuta, desde la consola, de dos formas:
  
  + ``` python addExp.py prueba```, para correr el programa con pairAndResInputs.txt
  
  + ``` python addExp.py biblia```, para correr el programa con pairAndResInputsBIBLIA.txt
  
  + Si queremos nuevos trials para la prueba tenemos que correr el generador de pares haciendo ``` python generadoresDePares.py     cantidad_de_pares_a_generar ``` donde cantidad_de_pares_a_generar >= 0.
  
  + Finalizado el experimento, si queremos analizar los resultados del mismo, tenemos que mover el archivo de resultados a la       carpeta Resultados.
  
  + Para analizar lo contenido en la carpeta Resultados, hacemos ``` python analizador_csv.py ``` desde la consola.
  
  + Deberíamos ver muchos gráficos.
