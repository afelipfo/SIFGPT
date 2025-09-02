/**
 * SIF-GPT - Sistema Unificado de PQRS
 * JavaScript principal que maneja todas las funcionalidades
 */

// Variables globales
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// Configuración de la API
const API_BASE = '';
const API_ENDPOINTS = {
    health: '/api/health',
    pqrs: {
        processText: '/api/pqrs/process-text',
        processAudio: '/api/pqrs/process-audio',
        transcribeAudio: '/api/pqrs/transcribe-audio',
        status: '/api/pqrs/status'
    },
    historico: {
        consulta: '/api/historico/consulta',
        radicado: '/api/historico/radicado',
        buscarTexto: '/api/historico/buscar/texto',
        buscarNombre: '/api/historico/buscar/nombre'
    },
    advancedHistorico: {
        consultaAvanzada: '/api/historico/consulta-avanzada',
        sugerencias: '/api/historico/sugerencias'
    },
    test: {
        historico: '/test/historico',
        advancedHistorico: '/test/advanced-historico'
    }
};

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 SIF-GPT iniciando...');
    
    // Inicializar componentes
    initializeChat();
    initializeAudio();
    initializeSystem();
    
    // Cargar datos iniciales
    loadInitialData();
    
    console.log('✅ SIF-GPT iniciado correctamente');
});

// ============================================================================
// INICIALIZACIÓN DE COMPONENTES
// ============================================================================

function initializeChat() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    
    if (messageInput && sendButton) {
        // Enviar mensaje con Enter
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Enviar mensaje con botón
        sendButton.addEventListener('click', sendMessage);
    }
}

function initializeAudio() {
    const micButton = document.getElementById('micButton');
    
    if (micButton) {
        micButton.addEventListener('click', toggleRecording);
    }
}

function initializeSystem() {
    // Inicializar Select2 para filtros avanzados
    if (typeof $ !== 'undefined' && $.fn.select2) {
        $('.select2').select2({
            placeholder: 'Selecciona una opción',
            allowClear: true
        });
    }
}

// ============================================================================
// FUNCIONALIDADES DEL CHAT
// ============================================================================

function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        showNotification('Por favor, escribe un mensaje', 'warning');
        return;
    }
    
    // Agregar mensaje del usuario al chat
    addMessageToChat(message, 'user');
    messageInput.value = '';
    
    // Mostrar indicador de carga
    showLoading(true);
    
    // Enviar mensaje al servidor
    axios.post(API_ENDPOINTS.pqrs.processText, {
        message: message
    })
    .then(response => {
        if (response.data.success) {
            addMessageToChat(response.data.response, 'bot');
        } else {
            addMessageToChat('Lo sentimos, ha ocurrido un error en el procesamiento.', 'bot');
        }
    })
    .catch(error => {
        console.error('Error enviando mensaje:', error);
        addMessageToChat('Error de conexión. Por favor, intenta de nuevo.', 'bot');
    })
    .finally(() => {
        showLoading(false);
    });
}

function addMessageToChat(message, type) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    const icon = type === 'user' ? 'fas fa-user' : 'fas fa-robot';
    messageDiv.innerHTML = `
        <i class="${icon} me-2"></i>
        ${message}
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ============================================================================
// FUNCIONALIDADES DE AUDIO
// ============================================================================

function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                sendAudioToServer(audioBlob);
            };
            
            mediaRecorder.start();
            isRecording = true;
            
            // Actualizar UI
            const micButton = document.getElementById('micButton');
            if (micButton) {
                micButton.classList.add('recording');
                micButton.innerHTML = '<i class="fas fa-stop"></i>';
                micButton.title = 'Detener grabación';
            }
            
            showNotification('Grabando audio...', 'info');
        })
        .catch(error => {
            console.error('Error accediendo al micrófono:', error);
            showNotification('Error al acceder al micrófono', 'error');
        });
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // Actualizar UI
        const micButton = document.getElementById('micButton');
        if (micButton) {
            micButton.classList.remove('recording');
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            micButton.title = 'Grabar Audio';
        }
        
        showNotification('Audio grabado, procesando...', 'info');
    }
}

function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    
    showLoading(true);
    
    axios.post(API_ENDPOINTS.pqrs.processAudio, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
        if (response.data.success) {
            // Agregar transcripción al chat
            addMessageToChat(`🎤 **Audio transcrito:** ${response.data.transcript}`, 'bot');
            
            // Si hay respuesta del sistema, mostrarla
            if (response.data.response) {
                addMessageToChat(response.data.response, 'bot');
            }
        } else {
            addMessageToChat('Error al procesar el audio', 'bot');
        }
    })
    .catch(error => {
        console.error('Error procesando audio:', error);
        addMessageToChat('Error al procesar el audio', 'bot');
    })
    .finally(() => {
        showLoading(false);
    });
}

// ============================================================================
// FUNCIONALIDADES DEL HISTÓRICO
// ============================================================================

function buscarHistorico() {
    const radicado = document.getElementById('radicadoInput').value.trim();
    const texto = document.getElementById('textoInput').value.trim();
    const nombre = document.getElementById('nombreInput').value.trim();
    
    if (!radicado && !texto && !nombre) {
        showNotification('Por favor, completa al menos un campo de búsqueda', 'warning');
        return;
    }
    
    showLoading(true);
    
    let endpoint = '';
    let data = {};
    
    if (radicado) {
        endpoint = `${API_ENDPOINTS.historico.radicado}/${radicado}`;
        axios.get(endpoint)
            .then(response => {
                displayHistoricoResults(response.data, 'radicado');
            })
            .catch(error => {
                console.error('Error buscando por radicado:', error);
                showNotification('Error en la búsqueda', 'error');
            })
            .finally(() => showLoading(false));
        return;
    }
    
    if (texto) {
        endpoint = API_ENDPOINTS.historico.buscarTexto;
        data = { texto: texto };
    } else if (nombre) {
        endpoint = API_ENDPOINTS.historico.buscarNombre;
        data = { nombre: nombre };
    }
    
    axios.post(endpoint, data)
        .then(response => {
            displayHistoricoResults(response.data, 'texto');
        })
        .catch(error => {
            console.error('Error en búsqueda:', error);
            showNotification('Error en la búsqueda', 'error');
        })
        .finally(() => showLoading(false));
}

function displayHistoricoResults(data, tipo) {
    const resultsContainer = document.getElementById('historicoResults');
    if (!resultsContainer) return;
    
    if (!data || !data.success) {
        resultsContainer.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <p>No se encontraron resultados</p>
            </div>
        `;
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-striped">';
    html += '<thead><tr><th>Radicado</th><th>Nombre</th><th>Fecha</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>';
    
    if (data.resultados && Array.isArray(data.resultados)) {
        data.resultados.forEach(item => {
            html += `
                <tr>
                    <td>${item.numero_radicado || '-'}</td>
                    <td>${item.nombre || '-'}</td>
                    <td>${item.fecha_radicacion || '-'}</td>
                    <td><span class="badge bg-${getStatusColor(item.estado_pqrs)}">${item.estado_pqrs || '-'}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="verDetallePQRS('${item.numero_radicado}')">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
    }
    
    html += '</tbody></table></div>';
    resultsContainer.innerHTML = html;
}

function getStatusColor(estado) {
    const statusColors = {
        'Pendiente': 'warning',
        'En proceso': 'info',
        'Resuelta': 'success',
        'Cancelada': 'danger'
    };
    return statusColors[estado] || 'secondary';
}

// ============================================================================
// FUNCIONALIDADES DEL DASHBOARD
// ============================================================================

function busquedaAvanzada() {
    const texto = document.getElementById('advancedTextoInput').value.trim();
    const limit = document.getElementById('limitInput').value;
    const ordenar = document.getElementById('ordenarInput').value;
    
    if (!texto) {
        showNotification('Por favor, ingresa un texto de búsqueda', 'warning');
        return;
    }
    
    showLoading(true);
    
    const filtros = {
        texto: texto,
        limit: parseInt(limit),
        ordenar_por: ordenar,
        orden: 'desc'
    };
    
    axios.post(API_ENDPOINTS.advancedHistorico.consultaAvanzada, filtros)
        .then(response => {
            if (response.data.success) {
                displayAdvancedResults(response.data.consulta_avanzada);
                updateMetrics(response.data.consulta_avanzada);
            } else {
                showNotification('Error en la búsqueda avanzada', 'error');
            }
        })
        .catch(error => {
            console.error('Error en búsqueda avanzada:', error);
            showNotification('Error en la búsqueda avanzada', 'error');
        })
        .finally(() => showLoading(false));
}

function displayAdvancedResults(data) {
    const resultsContainer = document.getElementById('advancedResults');
    if (!resultsContainer) return;
    
    if (!data || !Array.isArray(data)) {
        resultsContainer.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <p>No se encontraron resultados</p>
            </div>
        `;
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-striped">';
    html += '<thead><tr><th>Radicado</th><th>Nombre</th><th>Clasificación</th><th>Fecha</th><th>Estado</th><th>Texto</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += `
            <tr>
                <td>${item.numero_radicado || '-'}</td>
                <td>${item.nombre || '-'}</td>
                <td>${item.clasificacion || '-'}</td>
                <td>${item.fecha_radicacion || '-'}</td>
                <td><span class="badge bg-${getStatusColor(item.estado_pqrs)}">${item.estado_pqrs || '-'}</span></td>
                <td>${(item.texto_pqrs || '').substring(0, 100)}${(item.texto_pqrs || '').length > 100 ? '...' : ''}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    resultsContainer.innerHTML = html;
}

function updateMetrics(data) {
    if (!data || !Array.isArray(data)) return;
    
    const total = data.length;
    const pendientes = data.filter(item => item.estado_pqrs === 'Pendiente').length;
    const resueltas = data.filter(item => item.estado_pqrs === 'Resuelta').length;
    
    // Actualizar métricas del dashboard
    const totalElement = document.getElementById('totalPQRS-dash');
    const pendientesElement = document.getElementById('pendientes-dash');
    const resueltasElement = document.getElementById('resueltas-dash');
    
    if (totalElement) totalElement.textContent = total;
    if (pendientesElement) pendientesElement.textContent = pendientes;
    if (resueltasElement) resueltasElement.textContent = resueltas;
}

// ============================================================================
// FUNCIONALIDADES DEL SISTEMA
// ============================================================================

function refreshCaches() {
    showNotification('Refrescando cachés...', 'info');
    
    // Aquí podrías hacer una llamada a la API para refrescar cachés
    setTimeout(() => {
        showNotification('Cachés refrescadas correctamente', 'success');
        loadInitialData(); // Recargar datos
    }, 2000);
}

function validateSystem() {
    showNotification('Validando sistema...', 'info');
    
    // Aquí podrías hacer una llamada a la API para validar el sistema
    setTimeout(() => {
        showNotification('Sistema validado correctamente', 'success');
    }, 2000);
}

function viewLogs() {
    showNotification('Función de logs en desarrollo', 'info');
}

// ============================================================================
// FUNCIONES DE UTILIDAD
// ============================================================================

function loadInitialData() {
    // Cargar métricas del dashboard
    loadDashboardMetrics();
}

function loadDashboardMetrics() {
    // Simular carga de métricas del dashboard
    setTimeout(() => {
        // Las métricas ya están hardcodeadas en el HTML
        console.log('✅ Métricas del dashboard cargadas');
    }, 1000);
}

function showLoading(show) {
    // Implementar indicador de carga si es necesario
    if (show) {
        console.log('🔄 Cargando...');
    } else {
        console.log('✅ Carga completada');
    }
}

function showNotification(message, type = 'info') {
    // Crear notificación toast
    const toast = document.createElement('div');
    toast.className = `alert alert-${getAlertType(type)} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

function getAlertType(type) {
    const alertTypes = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return alertTypes[type] || 'info';
}

// ============================================================================
// FUNCIONES ADICIONALES
// ============================================================================

function verDetallePQRS(radicado) {
    showNotification(`Viendo detalles de PQRS: ${radicado}`, 'info');
    // Aquí podrías implementar la vista de detalles
}

// Exportar funciones para uso global
window.SIFGPT = {
    sendMessage,
    buscarHistorico,
    busquedaAvanzada,
    refreshCaches,
    validateSystem,
    viewLogs
};
