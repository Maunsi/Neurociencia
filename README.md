# Neurociencia o una experiencia subliminal

  [Hoja de ruta](#hoja-de-ruta)

  [Nota para correr el experimento](#nota-para-correr-el-experimento)

  [Agregar cambios o actualizar git](#agregar-cambios-o-actualizar-git)


### Hoja de ruta

- [ ] Cambios en el experimento: máscara($$$$$$), consignas, reducir a la mitad en ángulo visual de los flankers(medio metro).

- [ ] Buscar más víctimas.

- [ ] Ir definiendo el paper en paralelo a los puntos anteriores.

- [ ] Analizar los nuevos resultados.

- [ ] Armar presentación definitiva.

- [ ] Dar charla y presentar el paper.


### Nota para correr el experimento

El programa se ejecuta, desde la consola, de dos formas:
  
  + ``` python addExp.py prueba```, para correr el programa con pairAndResInputs.txt
  
  + ``` python addExp.py biblia```, para correr el programa con pairAndResInputsBIBLIA.txt
  
  + Si queremos nuevos trials para la prueba tenemos que correr el generador de pares haciendo ``` python generadoresDePares.py     cantidad_de_pares_a_generar ``` donde cantidad_de_pares_a_generar >= 0.
  
  + Finalizado el experimento, si queremos analizar los resultados del mismo, tenemos que mover el archivo de resultados a la       carpeta Resultados.
  
  + Para analizar lo contenido en la carpeta Resultados, hacemos ``` python analizador_csv.py ``` desde la consola.
  
  + Deberíamos ver muchos gráficos.

### Agregar cambios o actualizar git 

#### Agregar nuestros cambios a git

Desde la terminal, ubicados en la carpeta Neurocienca hacemos:
  
  + ``` git add archivos_que_queremos subir ``` o ``` git add . ``` para actualizar todos los archivos.
    Si queremos subir más de un archivo(pero no todos) basta con hacer ``` git add archivo1 archivo2 ... archivoN ```.
    
  + ``` git commit -m "mensaje que explique los cambios" ```, es importante que el mensaje con los cambios tenga comillas. Si       nos abre un editor de texto: escribir ahí el mensaje con los cambios.
  
  + ``` git push```, para subir nuestros cambios a git.
  
#### Actualizar nuestros archivos a la versión de git

Nos basta con hacer ``` git pull ```.

