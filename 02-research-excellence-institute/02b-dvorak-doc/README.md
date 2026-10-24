# Dr. Dvorak's Document — Research Excellence Institute

**Categoría:** Research Excellence Institute  
**Puntos:** 1  
**Flag:** `FLAG{BCjM-6SpO-HVpI-N13B}`

---

## 1. Descripción

> Hi Associate Researcher,
>
> The National Research and Education Network (NREN) has many experts, such as is Dr. Simon Dvorak, Chair of the Committee for Strategic QWERTY Decommissioning, member of 17 working groups, editor of 42 draft documents, and self-proclaimed "Home Row Evangelist".
>
> Yesterday, Dr. Dvorak briefly visited a shared workstation in the NREN office. Without looking at the keyboard, he quickly typed an important document, saved it, and left for following National QWERTY Transition Initiative meeting.
>
> Unfortunately, the resulting document appears to be complete nonsense. Your task is to recover the correct document.
>
> Stay curious!
>
> Download the [typed document](https://owncloud.cesnet.cz/index.php/s/bxY0ZfocJGyLqmu/download).  
> (SHA256 fingerprint `1b10f088e53772993ed6b628e9cb4f2846f848d203a4f94248ae90baeaa83fed`)

> **Hint 1 (0 pts):** The workstation was configured with the standard QWERTY layout.
>
> **Hint 2 (0 pts):** Mr. Dvorak produced the document at an astonishing speed while several of Dvorak enthusiasts chanted in support "One layout! One home row! Dvorak Simplified!".

---

## 2. Solución

### Identificar el problema

El Dr. Dvorak usa el layout de teclado **Dvorak** con total memoria muscular. La estación de trabajo compartida estaba configurada con **QWERTY**. Al escribir sin mirar, cada tecla que presionó produjo el carácter QWERTY correspondiente a esa posición física, no el carácter Dvorak que él intentó escribir.

**Ejemplo:** Para escribir `f` (que en Dvorak está en la posición de `y` en QWERTY), el Dr. Dvorak presionó la tecla en esa posición física → el sistema registró `y`.

### Pasos

1. **Descargar el archivo** (ZIP disfrazado de .txt):
   ```bash
   curl -sL "https://owncloud.cesnet.cz/index.php/s/bxY0ZfocJGyLqmu/download" -o document.zip
   unzip document.zip
   ```
   Contiene `dr_dvoraks_document.txt` con texto ilegible tipo:
   ```
   Hdao isspdaufd;w ;frrsokdo;w alh kjs;d...
   ```

2. **Construir el mapeo QWERTY → Dvorak** por posición física de tecla:

   | Fila | QWERTY | Dvorak |
   |------|--------|--------|
   | Números | `` `1234567890-= `` | `` `1234567890[] `` |
   | Superior | `qwertyuiop[]\` | `',.pyfgcrl/=\` |
   | Home | `asdfghjkl;'` | `aoeuidhtns-` |
   | Inferior | `zxcvbnm,./` | `;qjkxbmwvz` |

3. **Aplicar el mapeo** con el script `decode.py`:
   ```bash
   python3 decode.py dr_dvoraks_document.txt
   ```

4. El texto recuperado contiene la flag:
   ```
   Stay strong, think about FLAG{BCjM-6SpO-HVpI-N13B}.
   ```

5. **Submitir** la flag → **Correct**.

---

## 3. Notas

- El truco clave es recordar que el mapeado es **posición física → carácter del layout alternativo**. No es un cifrado, es un layout swap.
- El archivo descargado es un **ZIP** con extensión `.txt` — siempre verificar con `file` antes de asumir el formato.
- La conversión aplica a **todos los caracteres imprimibles**, incluyendo mayúsculas, signos de puntuación y símbolos (con Shift), excepto números que coinciden en ambos layouts.
- Herramienta útil para verificar: [kbd-audio layout tester](https://kbd.io) o simplemente Python con un dict de mapeo explícito.

---

## 4. Referencias

- Dvorak keyboard layout: https://en.wikipedia.org/wiki/Dvorak_keyboard_layout
- QWERTY vs Dvorak key mapping: https://www.dvorak-keyboard.com/
- Online converter QWERTY↔Dvorak: https://wbic16.xedoloh.com/dvorak.html

---

## Artefactos

| Archivo | Descripción |
|---------|-------------|
| `document.txt` | Archivo descargado del CTFd (ZIP con extensión .txt) |
| `document_original.zip` | Copia renombrada correctamente como ZIP |
| `dr_dvoraks_document_scrambled.txt` | Texto extraído del ZIP (scrambled) |
| `decode.py` | Script Python para decodificar QWERTY→Dvorak |
