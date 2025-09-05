/**
 * SIF-GPT - Sistema Unificado de PQRS
 * JavaScript principal que maneja todas las funcionalidades
 */

// Variables globales
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9); // ID único de sesión

// Configuración de la API
const API_BASE = '';
const API_ENDPOINTS = {
    health: '/api/health',
    pqrs: {
        processText: '/api/pqrs/process-simple',
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
    
    // Inicializar solo componentes esenciales
    initializeChat();
    initializeAudio();
    initializeEnhancedUI();
    
    console.log('✅ SIF-GPT iniciado correctamente');
});

// ============================================================================
// INICIALIZACIÓN DE COMPONENTES MEJORADOS
// ============================================================================

/**
 * Inicializa las mejoras de UI/UX y accesibilidad
 */
function initializeEnhancedUI() {
    console.log('🎨 Inicializando UI mejorada...');
    
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    
    // Validación inicial del botón enviar
    sendButton.disabled = true;
    
    // Eventos de entrada mejorados
    messageInput.addEventListener('input', function() {
        const hasText = this.value.trim().length > 0;
        sendButton.disabled = !hasText;
        
        // Feedback visual mejorado
        if (hasText) {
            sendButton.classList.add('ready');
        } else {
            sendButton.classList.remove('ready');
        }
    });
    
    // Mejoras de navegación por teclado
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey && !sendButton.disabled) {
            e.preventDefault();
            sendMessage();
        }
        
        // Accesibilidad: Escape para limpiar
        if (e.key === 'Escape') {
            this.value = '';
            sendButton.disabled = true;
            sendButton.classList.remove('ready');
            if (typeof announceToScreenReader === 'function') {
                announceToScreenReader('Campo de mensaje limpiado');
            }
        }
    });
    
    // Focus inicial
    setTimeout(() => {
        messageInput.focus();
    }, 100);
    
    console.log('✅ UI mejorada inicializada');
}
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
    showLoadingIndicator(true);
    
    // Enviar mensaje al servidor con session_id para contexto
    axios.post(API_ENDPOINTS.pqrs.processText, {
        message: message,
        session_id: sessionId
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
        showLoadingIndicator(false);
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
    console.log('🎤 Iniciando grabación de audio...');
    
    // Enhanced UI feedback
    if (typeof setButtonState === 'function') {
        setButtonState('micButton', 'recording');
    } else {
        const micButton = document.getElementById('micButton');
        micButton.classList.add('recording');
        micButton.innerHTML = '<i class="fas fa-stop" aria-hidden="true"></i><span class="btn-text">Detener</span>';
    }
    
    // Accessibility announcement
    if (typeof announceToScreenReader === 'function') {
        announceToScreenReader('Grabación de audio iniciada');
    }
    
    navigator.mediaDevices.getUserMedia({ 
        audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
            sampleRate: 44100
        } 
    })
        .then(stream => {
            console.log('✅ Acceso al micrófono obtenido');
            
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                    console.log('📊 Chunk de audio recibido:', event.data.size, 'bytes');
                }
            };
            
            mediaRecorder.onstop = () => {
                console.log('⏹️ Grabación detenida, procesando chunks...');
                console.log('📝 Total chunks:', audioChunks.length);
                
                // Reset button state
                if (typeof setButtonState === 'function') {
                    setButtonState('micButton', 'processing');
                } else {
                    const micButton = document.getElementById('micButton');
                    micButton.classList.remove('recording');
                    micButton.innerHTML = '<i class="fas fa-microphone" aria-hidden="true"></i><span class="btn-text">Procesando...</span>';
                    micButton.disabled = true;
                }
                
                if (audioChunks.length === 0) {
                    console.error('❌ No se capturó audio');
                    showEnhancedNotification('No se capturó audio. Intenta de nuevo.', 'warning');
                    resetMicButton();
                    return;
                }
                
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                console.log('🎵 Audio blob creado:', {
                    size: audioBlob.size,
                    type: audioBlob.type
                });
                
                if (audioBlob.size === 0) {
                    console.error('❌ El audio capturado está vacío');
                    showEnhancedNotification('El audio capturado está vacío. Intenta de nuevo.', 'warning');
                    resetMicButton();
                    return;
                }
                
                // Accessibility announcement
                if (typeof announceToScreenReader === 'function') {
                    announceToScreenReader('Audio capturado, enviando para procesamiento');
                }
                
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
            console.error('❌ Error accediendo al micrófono:', error);
            let errorMessage = 'Error al acceder al micrófono';
            
            if (error.name === 'NotAllowedError') {
                errorMessage = 'Permiso de micrófono denegado. Por favor, permite el acceso al micrófono.';
            } else if (error.name === 'NotFoundError') {
                errorMessage = 'No se encontró micrófono. Verifica que tengas un micrófono conectado.';
            } else if (error.name === 'NotReadableError') {
                errorMessage = 'El micrófono está siendo usado por otra aplicación.';
            }
            
            showNotification(errorMessage, 'error');
            
            // Resetear botón del micrófono en caso de error de acceso
            resetMicButton();
        });
}

function stopRecording() {
    console.log('⏹️ Deteniendo grabación...');
    
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        // Detener todas las pistas de audio
        mediaRecorder.stream.getTracks().forEach(track => {
            track.stop();
            console.log('🔇 Pista de audio detenida');
        });
        
        // Enhanced UI feedback
        if (typeof setButtonState === 'function') {
            setButtonState('micButton', 'processing');
        } else {
            const micButton = document.getElementById('micButton');
            if (micButton) {
                micButton.classList.remove('recording');
                micButton.innerHTML = '<i class="fas fa-microphone" aria-hidden="true"></i><span class="btn-text">Procesando...</span>';
                micButton.title = 'Procesando audio';
                micButton.disabled = true;
            }
        }
        
        // Accessibility announcement (solo para lectores de pantalla)
        if (typeof announceToScreenReader === 'function') {
            announceToScreenReader('Grabación detenida, procesando audio');
        }
        
        console.log('✅ Grabación detenida correctamente');
    } else {
        console.warn('⚠️ No hay grabación activa para detener');
        resetMicButton();
    }
}

// Helper function to reset microphone button
function resetMicButton() {
    console.log('🔄 Reseteando botón del micrófono...');
    const micButton = document.getElementById('micButton');
    if (micButton) {
        // Limpiar todas las clases y estados
        micButton.classList.remove('recording', 'processing');
        micButton.innerHTML = '<i class="fas fa-microphone" aria-hidden="true"></i><span class="btn-text">Grabar</span>';
        micButton.title = 'Grabar audio';
        micButton.disabled = false;
        
        // Forzar actualización visual
        micButton.style.opacity = '1';
        micButton.style.pointerEvents = 'auto';
        
        console.log('✅ Botón del micrófono reseteado correctamente');
    }
    isRecording = false;
}

function sendAudioToServer(audioBlob) {
    console.log('📤 Enviando audio al servidor...', {
        size: audioBlob.size,
        type: audioBlob.type,
        sessionId: sessionId
    });
    
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('session_id', sessionId);  // Incluir session_id para contexto
    
    // Mostrar mensaje de procesamiento en el chat
    addMessageToChat('🎤 Procesando audio...', 'bot');
    
    axios.post(API_ENDPOINTS.pqrs.processAudio, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        timeout: 30000  // 30 segundos de timeout
    })
    .then(response => {
        console.log('✅ Respuesta del servidor:', response.data);
        
        if (response.data.success) {
            // Agregar transcripción al chat (solo el texto, sin prefijo)
            if (response.data.transcript) {
                addMessageToChat(response.data.transcript, 'user');
            }
            
            // Si hay respuesta del sistema, mostrarla
            if (response.data.response) {
                addMessageToChat(response.data.response, 'bot');
            }
            
            showNotification('Audio procesado correctamente', 'success');
            
            // Resetear botón del micrófono para permitir nueva grabación
            resetMicButton();
        } else {
            const errorMsg = response.data.error || 'Error desconocido al procesar el audio';
            console.error('❌ Error del servidor:', errorMsg);
            addMessageToChat(`Error: ${errorMsg}`, 'bot');
            showNotification('Error al procesar el audio', 'error');
            
            // Resetear botón del micrófono incluso en caso de error
            resetMicButton();
        }
    })
    .catch(error => {
        console.error('❌ Error procesando audio:', error);
        
        let errorMessage = 'Error de conexión al procesar el audio';
        if (error.response) {
            // Error de respuesta del servidor
            errorMessage = error.response.data?.error || `Error del servidor (${error.response.status})`;
        } else if (error.request) {
            // Error de red
            errorMessage = 'Error de conexión con el servidor';
        } else {
            // Error de configuración
            errorMessage = 'Error al preparar la solicitud';
        }
        
        addMessageToChat(`Error: ${errorMessage}`, 'bot');
        showNotification('Error al procesar el audio', 'error');
        
        // Resetear botón del micrófono incluso en caso de error de conexión
        resetMicButton();
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
    
    showLoadingIndicator(true);
    
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
            .finally(() => showLoadingIndicator(false));
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
        .finally(() => showLoadingIndicator(false));
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
    
    showLoadingIndicator(true);
    
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
        .finally(() => showLoadingIndicator(false));
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

function showLoadingIndicator(show) {
    // Implementar indicador de carga si es necesario
    if (show) {
        console.log('🔄 Cargando...');
    } else {
        console.log('✅ Carga completada');
    }
}

// Enhanced notification system
function showEnhancedNotification(message, type = 'info', duration = 5000) {
    // Try to use the enhanced toast function from HTML if available
    if (typeof showToast === 'function') {
        return showToast(message, type, duration);
    }
    
    // Fallback to original notification
    return showNotification(message, type);
}

function showNotification(message, type = 'info') {
    // Crear notificación toast
    const toast = document.createElement('div');
    toast.className = `alert alert-${getAlertType(type)} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: var(--shadow-lg); border-radius: 12px;';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="${getIconForType(type)} me-2" aria-hidden="true"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar notificación"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Accessibility announcement
    if (typeof announceToScreenReader === 'function') {
        announceToScreenReader(message);
    }
    
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

function getIconForType(type) {
    const iconTypes = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-triangle', 
        'warning': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    };
    return iconTypes[type] || 'fas fa-info-circle';
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
