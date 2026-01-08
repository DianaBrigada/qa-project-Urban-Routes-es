# 🚕 Urban Routes – QA Automation Project

## 📌 Descripción del Proyecto
**Urban Routes** es un proyecto de **automatización de pruebas end-to-end** que valida el flujo completo de solicitud de un **servicio de taxi en línea**.  
El objetivo principal es asegurar el correcto funcionamiento del proceso de reserva, verificando cada una de las interacciones del usuario desde la configuración de direcciones hasta la confirmación del servicio.

Las pruebas automatizadas validan acciones como:
- Ingreso y validación de direcciones
- Selección de tarifas
- Interacción con botones y formularios
- Ingreso de datos de contacto
- Comunicación con el conductor para solicitudes adicionales
- Métodos de pago
- Confirmación de la reserva del servicio

---

## 🧪 Alcance de las Pruebas
Las pruebas cubren el flujo completo de solicitud de un taxi, incluyendo:

- Configuración de la dirección de origen y destino
- Selección de la tarifa **Comfort**
- Registro del número de teléfono
- Agregado de tarjeta de crédito
- Envío de mensajes al conductor
- Solicitud de servicios adicionales (manta y pañuelos)
- Pedido de 2 helados
- Espera y validación de la búsqueda de un taxi

---

## 📂 Estructura del Proyecto

```text
qa-project-Urban-Routes/
│
├── data.py          # Datos utilizados en las pruebas
├── locators.py      # Localizadores de los elementos de la página
├── helpers.py       # Funciones auxiliares (ej. obtención de código de confirmación)
├── methods.py       # Métodos reutilizables para las pruebas
├── test_main.py     # Casos de prueba y validaciones principales
└── README.md        # Documentación del proyecto

