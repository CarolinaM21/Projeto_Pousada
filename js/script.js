// script.js

// Função para redirecionar para a página de cadastro com dados do formulário
function simulateBooking(event, roomType, price) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Pega o formulário específico que disparou o evento
    const form = event.target;

    // Captura os valores dos campos dentro do formulário
    const checkin = form.querySelector('input[name="checkin"]').value;
    const checkout = form.querySelector('input[name="checkout"]').value;
    const adults = form.querySelector('select[name="adults"]').value;

    // Verifica se os campos estão preenchidos
    if (checkin && checkout && adults) {
        // Redireciona para a página de cadastro com parâmetros na URL
        window.location.assign(`cadastro_reserva.html?room=${roomType}&price=${price}&checkin=${checkin}&checkout=${checkout}&adults=${adults}`);
    } else {
        alert("Por favor, preencha todos os campos.");
    }
}
