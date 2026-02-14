"""
leerdatos.py

Script sencillo para cargar y analizar el archivo `datos_sinteticos.csv`.

Funciones:
- Cargar CSV con pandas
- Mostrar las 5 primeras filas
- Resumen: forma, tipos, valores nulos, estadísticas descriptivas
- Conteos para variables categóricas
- Detección de duplicados
- Gráficas (guardadas en ./output): histogramas, boxplots y mapa de correlación

Si faltan dependencias imprime instrucciones para instalarlas.
"""

from pathlib import Path
import sys
import traceback


def main():
	try:
		import pandas as pd
		import matplotlib.pyplot as plt
		import seaborn as sns
	except Exception as e:
		print("Faltan dependencias necesarias para ejecutar el análisis.")
		print("Instala las librerías con:\n    pip install pandas matplotlib seaborn")
		print("Error de importación:", e)
		return

	sns.set(style="whitegrid")

	base = Path(__file__).resolve().parent
	csv_path = base / "datos_sinteticos.csv"

	if not csv_path.exists():
		print(f"No se encontró el archivo: {csv_path}")
		return

	print(f"Cargando: {csv_path}\n")
	# Intentar inferir separador y codificación de forma simple
	try:
		df = pd.read_csv(csv_path)
	except Exception:
		# Intentar con sep=';' por si es CSV separado por punto y coma
		try:
			df = pd.read_csv(csv_path, sep=';')
		except Exception:
			print("Error leyendo el CSV. Mostrar traceback:")
			traceback.print_exc()
			return

	out_dir = base / "output"
	out_dir.mkdir(exist_ok=True)

	# 1) Primeras 5 filas
	print("Primeras 5 filas:")
	print(df.head(5).to_string(index=False))
	print("\n---\n")

	# 2) Forma y tipos
	print("Dimensiones (filas, columnas):", df.shape)
	print("\nTipos de columnas:")
	print(df.dtypes)
	print("\n---\n")

	# 3) Valores nulos
	print("Valores nulos por columna:")
	print(df.isnull().sum())
	print("\n---\n")

	# 4) Estadísticas descriptivas para columnas numéricas
	print("Estadísticas descriptivas (numéricas):")
	print(df.describe(include='number').transpose())
	print("\n---\n")

	# 5) Estadísticas para columnas no numéricas
	print("Estadísticas (no numéricas):")
	print(df.describe(include=['object', 'category']))
	print("\n---\n")

	# 6) Detección de duplicados
	dup_count = df.duplicated().sum()
	print(f"Filas duplicadas: {dup_count}")
	if dup_count > 0:
		print("Ejemplo de filas duplicadas:")
		print(df[df.duplicated()].head().to_string(index=False))

	# 7) Conteos para columnas categóricas (si pocas categorías)
	cat_cols = [c for c in df.columns if df[c].dtype == 'object' or str(df[c].dtype).startswith('category')]
	if cat_cols:
		print("\nConteos para columnas categóricas (primeras 10 categorías si existen):")
		for c in cat_cols:
			print(f"\nColumna: {c}")
			print(df[c].value_counts(dropna=False).head(10))

	# 8) Gráficas para columnas numéricas
	num_cols = df.select_dtypes(include='number').columns.tolist()
	if num_cols:
		print("\nGenerando histogramas y boxplots para columnas numéricas (guardados en ./output)")
		for c in num_cols:
			plt.figure(figsize=(8, 4))
			sns.histplot(df[c].dropna(), kde=True)
			plt.title(f"Histograma: {c}")
			plt.tight_layout()
			fn = out_dir / f"hist_{c}.png"
			plt.savefig(fn)
			plt.close()

			plt.figure(figsize=(6, 4))
			sns.boxplot(x=df[c].dropna())
			plt.title(f"Boxplot: {c}")
			plt.tight_layout()
			fn = out_dir / f"box_{c}.png"
			plt.savefig(fn)
			plt.close()

		# Correlación
		if len(num_cols) > 1:
			print("Generando mapa de correlación (guardado en ./output/correlation_matrix.png)")
			corr = df[num_cols].corr()
			plt.figure(figsize=(max(6, len(num_cols)), max(4, len(num_cols) / 2)))
			sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True)
			plt.title('Matriz de correlación')
			plt.tight_layout()
			plt.savefig(out_dir / 'correlation_matrix.png')
			plt.close()

	else:
    		print("No se detectaron columnas numéricas para graficar.")

	print(f"\nAnálisis completado. Archivos de salida en: {out_dir}")


if __name__ == '__main__':
	main()