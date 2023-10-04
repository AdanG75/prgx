

- Utilizando nombre genéricos de tablas como dbo.Table_test, dbo.Table _final realiza cual sería un proceso de compresión de tabla desde la tabla test hacia la Final, son solo 3 pasos escribelos

  1.- Instalar la extensión pg_compress:


  ```sql
  CREATE EXTENSION IF NOT EXISTS pg_compression;
  ```
  2.- Crear la nueva tabla con compresión:
  
  ```sql
      CREATE TABLE dbo.Table_final
      AS SELECT * FROM dbo.Table_test
      WITH (compressed);
  ```
  
  3.- Copiar los datos:


  ```sql
  INSERT INTO dbo.Table_final
  SELECT * FROM dbo.Table_test;
  ```

- Que tabla del Sistema te puede dar la información de los índices, escribe el código de la consulta

  ```sql
  -- Supuniendo que los índices se encuentran en el esquema público
  SELECT 
    schemaname AS esquema,
    tablename AS tabla,
    indexname AS nombre_indice,
    indexdef AS definicion_indice
  FROM 
    pg_indexes
  WHERE 
    schemaname = 'public';
  ```

- En pocas palabras describe la diferencia entre un Cluster y Non Cluster Index

  **Clustered Index** agrupa y ordena los índices alterando la formación física de la tabla. Solamente, puede ver un clustered index por tabla y se recomiendan para hacer consultas sobre toda la tabla
  **No Clustered Index** no agrupa los índices y por ende no acecta la estructura física de la tabla. Lo anterior permite tener varios índices de este tipo dentro una tabla. Ideal para realizar consultas a objetos especificos

- Respecto a la pregunta anterior escribe el código de un Cluster index (Nombre: C_INDX_VENDORNUMBER) y aplícale un método de compresión. “El nombre del índice te da la referencia del campo a utilizar”

  ```sql
  -- Crear el Clustered Index
  CREATE INDEX C_INDX_VENDORNUMBER
  ON mi_tabla
  USING btree (VENDOR_NUMBER);

  -- Aplicar el Clustered Index
  ALTER TABLE mi_tabla
  CLUSTER ON C_INDX_VENDORNUMBER;
  ```

- Identifica si hay errores en el siguiente código
  ```sql
  SELECT DISTINTC
  VENDOR_NUMBER,
  MAX(VENDOR_NAME) AS VENDOR_NAME
  SUM(QTY),
  SUM(CLAIM_AMOUNT) AS NETCLAIM_AMOUNT
  FROM dbo.P_LINEITEM
  GROUP BY VENDOR_NUMBER;
  ```
Rescribe el código si encontraste algún error:

  ```sql
  -- Eliminamos el DISTINCT ya que el GROUP BY se encargará de hacer la misma función de manera implícita. Para que esto no genere error, cada columna que no se encuetre marcado por el GROUP BY deberá tener una función de acumulación o agregación
  SELECT
    VENDOR_NUMBER,
    MAX(VENDOR_NAME) AS VENDOR_NAME,
    SUM(QTY) AS TOTAL_QTY,
    SUM(CLAIM_AMOUNT) AS NETCLAIM_AMOUNT
  FROM dbo.P_LINEITEM
  GROUP BY
    VENDOR_NUMBER;
  ```

Si tengo una tabla llamada dbo.Server1 en una base de datos Cliente_PROD_F en un servidor ATL20CX7890SQ26 y estoy en un servidor ATLCX3456SQ99 en una base de datos X selecciona las primeras 1000 líneas desde la base X hacia la tabla Server1 en su servidor a través de servidores linkeados
  
  ```sql
  INSERT INTO X.Server1
  SELECT * FROM dblink(
    'dbname=dbo
    port=5432
    host=ATL20CX7890SQ26
    user=my_user
    password=my_password',
    'SELECT * FROM dbo.Server1 LIMIT 1000;'
  );
  ```

