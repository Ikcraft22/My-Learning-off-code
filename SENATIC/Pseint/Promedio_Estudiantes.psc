	Proceso Promedio_Estudiantes
		
		Definir n, i, j Como Entero
		Definir nombres Como Cadena
		Definir notas, promedios Como Real
		
		// Pedir cantidad de estudiantes
		Escribir "Ingrese la cantidad de estudiantes:"
		Leer n
		
		// Dimensionar arreglos
		Dimension nombres[n]
		Dimension notas[n,3]
		Dimension promedios[n]
		
		
		Para i <- 0 Hasta n-1 Hacer
			
			Escribir "Ingrese el nombre del estudiante ", i+1, ":"
			Leer nombres[i]                          
			
			Para j <- 0 Hasta 2 Hacer
				Escribir "Ingrese la nota ", j+1, " del estudiante ", nombres[i], ":"
				Leer notas[i,j]
			FinPara
			
		FinPara
		
	
		Para i <- 0 Hasta n-1 Hacer
			promedios[i] <- 0
			
			Para j <- 0 Hasta 2 Hacer
				promedios[i] <- promedios[i] + notas[i,j]
			FinPara
			
			promedios[i] <- promedios[i] / 3
			
		FinPara
		
		
		Escribir "===== RESULTADOS ====="
		
		Para i <- 0 Hasta n-1 Hacer
			Escribir "Estudiante: ", nombres[i]
			Escribir "Promedio: ", promedios[i]
			Escribir "---------------------"
		FinPara
		
FinProceso

