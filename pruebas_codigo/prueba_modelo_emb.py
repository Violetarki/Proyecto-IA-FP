from src.rag.embeddings import cargar_modelo

modelo = cargar_modelo()
print("Límite de tokens del modelo:", modelo.max_seq_length)


texto_ejemplo = """ Beneficios no repartidos o reservas

Los beneficios empresariales son los ingresos netos que obtiene la empresa después de descontar todos los pagos, incluidos los impuestos. Habitualmente, un porcentaje de estos beneficios se reparte entre los socios y el otro se man tiene en la empresa como fondo para cubrir riesgos o para realizar nuevas inversiones, son las llamadas reservas.

Si no se utilizan todas las reservas, los excedentes monetarios se pueden depositar en algún producto bancario que ofrezca una mejor rentabilidad que una cuenta corriente. Algunas entidades bancarias denominan a este tipo de productos «Cuenta Negocios» como reclamo.

Ejemplo: Casbega, la embotelladora de Coca-Cola para el centro de España, apuesta por la inversión continua en innovación. En el último año, esta suma ascendió a 13 millones de euros, lo que supone casi el 20% de los beneficios de la firma. Esta partida se dedica, en parte, a mejorar su huella ecológica. «Buscamos conseguir envases más sostenibles, que minimicen el impacto ambiental», explica el director industrial. La vocación de la compañía por la innovación le ha permitido ser pionera dentro de su sector, lo que le ha servido para conseguir el sello de calidad de Madrid Excelente.

Fuente: Cinco Días. Madrid, 20 de diciembre de 2011 [en línea]

- Incorporación de nuevos socios o ampliación de capital

Vender una parte de la empresa para permitir la entrada de nuevos socios puede resultar de utilidad. En tal caso, la sociedad continúa siendo la misma, no hay cambio en la entidad sino en sus propietarios.

Sociedad limitada laboral limitada: las participaciones solo se pueden transmitir otros socios, al cónyuge los hijos.

Sociedad anónima laboral anónima: la transmisión de acciones es libre.

Las sociedades anónimas de grandes dimensiones ponen sus acciones en circulación través de los mercados de valores: la bolsa el Mercado Alternativo Bursátil (MAB).

Cotización en bolsa. Las sociedades anónimas que cumplen ciertos requisitos pueden vender sus acciones libremente en este mercado de valores. Es una opción para grandes empresas, puesto que se exige un capital mínimo superior 200000 euros. La entrada en bolsa puede suponer una importante vía de obtención de recursos, ya que los inversores están comprando una parte del accionariado de la empresa, con lo que se incrementa el capital de la compañía, si bien también genera una presión la gerencia de la empresa para tomar decisiones que sean bien acogidas por los accionistas para evitar acciones que puedan dañar su imagen.

Mercado Alternativo Bursátil (MAB). Las compañías de menor tamaño facturación pueden cotizar sus acciones en el MAB de manera similar como cotizan las grandes empresas en la bolsa.

Ejemplo: En bolsa cotizan empresas tan conocidas como Iberia, Campofrío, Zeltia, Antena 3, NH Hoteles, Repsol, Cepsa, Abertis, Ferrovial, Telefónica, Banco Santander, BBVA Corporación Mapfre. Imaginarium es una empresa que cotiza en el MAB, al igual que Zinkia (la empresa propietaria de los derechos de Pocoyó), Gowex (experta en servicios de red inalámbrica ciudades) Bodaclick (portal web dedicado la organización de bodas).

- Subvenciones

Las ayudas económicas que ofrece la Administración los organismos públicos tienen la ventaja de ser fondo perdido, es decir, que no tienen que ser devueltas, razón por la que se incluyen como un recurso propio.

Ejemplo: La Junta de Castilla León concedió en 2012,304560 euros en subvenciones ayuntamientos del medio rural con el fin de financiar las obras necesarias en centros educativos para poder impartir el primer ciclo de Educación Infantil. La Junta de Castilla y León financió el 90% del coste de la inversión, mientras que el 10 restante corrió cargo de cada ayuntamiento.

Tabla 4.2. Modos de financiación por capital arranque y capital de expansión (recursos propios).
"""
print("Caracteres:", len(texto_ejemplo))
tokens = modelo.tokenizer(texto_ejemplo)
print("Número de tokens:", len(tokens["input_ids"]))
