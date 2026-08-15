# Ingeniería social

La mayoría de brechas graves no empiezan con un exploit técnico sofisticado,
sino engañando a una persona. Es, con diferencia, el vector más efectivo.

## Principios psicológicos que se explotan

- **Autoridad**: hacerse pasar por un jefe, IT, o la policía — la gente obedece
  instrucciones de quien parece tener autoridad.
- **Urgencia/miedo**: "tu cuenta será suspendida en 1 hora" — no da tiempo a
  pensar con calma.
- **Prueba social**: "todos tus compañeros ya lo hicieron" — reduce la
  sospecha individual.
- **Reciprocidad**: dar algo pequeño (un "regalo", ayuda no pedida) para que
  la víctima se sienta en deuda y baje la guardia.
- **Simpatía/confianza**: construir rapport (llamadas de "soporte técnico"
  amables) antes de pedir la acción sensible.

## Técnicas concretas

- **Pretexting**: inventar una historia creíble (finge ser un proveedor, un
  nuevo empleado, un auditor) para conseguir información o acceso físico.
- **Baiting**: dejar un USB "perdido" con malware en el parking de una
  empresa, esperando que alguien lo conecte por curiosidad.
- **Tailgating/piggybacking**: seguir de cerca a un empleado para entrar a
  una zona con control de acceso sin usar credenciales propias.
- **Vishing**: llamadas telefónicas suplantando soporte técnico, un banco, o
  IT interno, para obtener credenciales o convencer de instalar software de
  acceso remoto.
- **Business Email Compromise (BEC)**: comprometer o suplantar el correo de
  un ejecutivo para ordenar una transferencia urgente a finanzas.

## Cómo se prepara un ataque de ingeniería social (OSINT)

Antes de contactar a la víctima, se recopila información pública:
LinkedIn (organigrama, quién es el jefe de quién), redes sociales
(intereses, vacaciones — "estás fuera esta semana, así que no puedes
verificar en persona"), metadatos de documentos públicos, y filtraciones de
datos previas.

## Defensa

- **Formación continua**, no solo un curso anual — simulaciones periódicas
  (como el demo de phishing) que midan y refuercen sin castigar a quien cae.
- **Verificación fuera de banda** para acciones sensibles: si "el CEO" pide
  una transferencia por correo, confirmar por teléfono con un número
  conocido de antemano, no el que venga en el mensaje.
- **Cultura de "está bien decir no" y preguntar**: que un empleado pueda
  frenar una petición urgente sin miedo a parecer poco colaborador.
- **Controles de proceso**, no solo de personas: doble aprobación para
  transferencias, no depender solo del criterio individual bajo presión.
- **Políticas físicas**: badges visibles, cultura de cuestionar a quien no
  reconoces cerca de zonas restringidas.
