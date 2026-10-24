# SALVOR

Sección resuelta y validada en CTFd. Los cuatro retos apuntan inicialmente a `http://intro.salvor.nren.tcc`; la navegación de esa página enlaza con DSRepos, el foothold SSH y el asistente de chat.

| Capítulo | Técnica | Flag |
|---|---|---|
| 1. Act-er | React Server Components / Server Action RCE | `FLAG{2cgd-Jb3C-0Tib-Iol9}` |
| 2. 'Bəfər | Lectura arbitraria mediante format string en proxy C | `FLAG{LWoM-kzkO-YFUf-XGpm}` |
| 3. Prompt | Prompt injection y decodificación NATO | `FLAG{dsNI-3wkY-KzHH-8sAu}` |
| 4. Raggad | Prompt injection sobre RAG y Base64 | `FLAG{TSPL-Gp8P-pLPJ-YdKy}` |

## Cadena de acceso

El primer reto expone una ejecución de comandos en DSRepos. Esa ejecución permitió leer la clave privada de `deploy` (se usó solo en memoria temporal, no se conserva en el repositorio) y entrar por SSH al host `dsrepos-foothold.salvor.nren.tcc`. Desde allí se identificó el proxy C en el puerto 3001. Los dos capítulos de chat se resolvieron mediante sus endpoints HTTP autorizados.

Detalles técnicos y comandos reproducibles están en los README de cada capítulo.
