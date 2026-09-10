# Especificación del producto

## Problema y usuario
Reclutadores y candidatos necesitan comparar evidencia explícita de un CV con un perfil de cargo sin depender de una respuesta libre o un puntaje arbitrario.

## Alcance
La aplicación recibe ambos textos, valida un mínimo de 100 caracteres, extrae indicadores, calcula un puntaje trazable y devuelve fortalezas, brechas, recomendaciones, advertencias y metadatos del modelo. PDF, autenticación y almacenamiento de CV quedan fuera de v1.

## Historias de usuario
1. Como reclutador, quiero comparar un CV con un perfil para priorizar una revisión humana.
2. Como candidato, quiero conocer brechas concretas para mejorar mi postulación.
3. Como evaluador, quiero repetir casos y consultar la fórmula para verificar el resultado.

## Escenarios Given/When/Then
1. Dado un CV compatible, cuando se analiza, entonces devuelve puntaje alto y coincidencias.
2. Dado un CV parcial, cuando se analiza, entonces devuelve puntaje medio y brechas.
3. Dado un CV no compatible, cuando se analiza, entonces devuelve puntaje bajo sin inventar datos.
4. Dado un texto menor a 100 caracteres, cuando se envía, entonces responde 422.
5. Dado un timeout del modelo, cuando se analiza, entonces responde 503.
6. Dado JSON inválido del proveedor, cuando se analiza, entonces responde 502.
7. Dado el servicio activo, cuando se consulta `/health`, entonces responde versión y disponibilidad.
8. Dados los fixtures, cuando se consulta `/api/v1/examples`, entonces devuelve casos alta, media y baja.

