Algoritmo reajuste_sueldo
	Definir sueldo,antiguedad,rsueldo Como Entero
	Escribir "PROGRAMA PARA REAJUSTAR EL SUELDO DEL EMPLEADO"
	Escribir "Digite el sueldo del empleado"
	Leer sueldo
	Escribir "Digite la antiguedad del empleado"
	Leer antiguedad
	Si (antiguedad <=10) Entonces
		Si (sueldo<=300000) Entonces
			rsueldo<-sueldo+(sueldo*0.12)
			Escribir "El reajuste para el empleado es: $" rsueldo
		SiNo
			Si(sueldo>300000) Y (sueldo<=500000)  Entonces
				rsueldo<-sueldo+(sueldo*0.10)
				Escribir "El reajuste para el empleado es: $" rsueldo
			SiNo
				Si (sueldo>500000) Entonces
					rsueldo<-sueldo+(sueldo*0.08)
					Escribir "El reajuste para el empleado es: $" rsueldo
				Fin Si
			Fin Si
		Fin Si
	SiNo
		Si (antiguedad>=10) Y (antiguedad<=20) Entonces
			Si (sueldo<=300000) Entonces
				rsueldo<-sueldo+(sueldo*0.14)
				Escribir "El reajuste para el empleado es: $" rsueldo
			SiNo
				Si (sueldo>300000) Y (sueldo<=500000)  Entonces
					rsueldo<-sueldo+(sueldo*0.12)
					Escribir "El reajuste para el empleado es: $" rsueldo
				SiNo
					Si (sueldo>500000) Entonces
						rsueldo<-sueldo+(sueldo*0.10)
						Escribir "El reajuste para el empleado es: $" rsueldo
					Fin Si
				Fin Si
			Fin Si
		SiNo
			Si (antiguedad>=20) Entonces
				rsueldo<-sueldo+(sueldo*0.15)
				Escribir "El reajuste para el empleado es: $" rsueldo
			Fin Si
		Fin Si
	Fin Si
FinAlgoritmo