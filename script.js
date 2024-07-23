// URL de Firebase para obtener el estado
const appStateUrl = 'https://biofacepro-default-rtdb.firebaseio.com/appstate/state.json?auth=blpAMq9G4AqyEPStZ5hsizUXyo8nq6lu06ZZJpzu';

// URL de Firebase para obtener los logs
const logsUrl = 'https://biofacepro-default-rtdb.firebaseio.com/logs.json?auth=blpAMq9G4AqyEPStZ5hsizUXyo8nq6lu06ZZJpzu';

// Rutas de las imágenes
const getFaceIdImage = 'imagenes//Reconocimiento.png';  // Imagen para estado getfaceid
const errorImage = 'imagenes//tarjeta_rechazada.webp'; // Imagen para estado error
const getCardImage = 'imagenes//esperando_tarjeta.webp';  // Imagen para estado getcard
const defaultImage = 'imagenes//check.webp';  // Imagen para estado true
const faceidnullImage = 'imagenes//faceidnull.jpg';  // Imagen para estado true
// Función para obtener el estado de Firebase
async function checkAppState() {
    try {
        const response = await fetch(appStateUrl);
        const state = await response.json();
        const imageElement = document.getElementById('status-image');
        const containerElement = document.getElementById('image-container');
        const statusTextElement = document.getElementById('status-text');

        // Cambiar la imagen, el estilo del contenedor y el texto basado en el estado
        switch(state) {
            case 'getfaceid':
                imageElement.src = getFaceIdImage;
                containerElement.className = 'status-getfaceid';
                statusTextElement.textContent = 'Realizando reconocimiento';
                break;
            case 'error':
                imageElement.src = errorImage;
                containerElement.className = 'status-error';
                statusTextElement.textContent = 'Tarjeta rechazada';
                break;
            case 'getcard':
                imageElement.src = getCardImage;
                containerElement.className = 'status-getcard';
                statusTextElement.textContent = 'Esperando tarjeta';
                break;
            case 'faceidnull':
                imageElement.src = faceidnullImage;
                containerElement.className = 'status-faceidnull';
                statusTextElement.textContent = 'Reconocimiento no exitoso';
                break;
            default:
                imageElement.src = defaultImage;
                containerElement.className = 'status-true';
                statusTextElement.textContent = 'Pago exitoso';
                break;
        }
    } catch (error) {
        console.error('Error al obtener el estado de Firebase:', error);
    }
}

// Llamar a la función para verificar el estado y los logs cuando la página se carga
document.addEventListener('DOMContentLoaded', () => {
    checkAppState();  // Verificar el estado al cargar la página
    // Actualizar el estado cada 1 segundo
    setInterval(checkAppState, 1000);
});
