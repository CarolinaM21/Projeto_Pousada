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
<script>
function simulateBooking(event, acomodacao, preco) {
    event.preventDefault(); // Impede o envio do formulário

    // Obtém os elementos do formulário
    const form = event.target;
    const checkinDate = new Date(form.checkin.value);
    const checkoutDate = new Date(form.checkout.value);
    const adults = form.adults.value;

    // Verifica se as datas são válidas
    if (isNaN(checkinDate) || isNaN(checkoutDate)) {
        alert("Por favor, selecione datas válidas.");
        return;
    }

    // Calcula a diferença em dias
    const days = (checkoutDate - checkinDate) / (1000 * 60 * 60 * 24);
    if (days <= 0) {
        alert("A data de check-out deve ser após a data de check-in.");
        return;
    }

    // Calcula o valor total
    const dailyRate = parseFloat(preco.replace("R$", "").replace(",", ".")); // Converte o preço para número
    const total = dailyRate * days;

    // Atualiza o conteúdo da div de resultado abaixo do formulário
    const resultDiv = form.nextElementSibling; // Seleciona a div booking-result
    resultDiv.innerHTML = `
        <h3>Simulação de Reserva para ${acomodacao}</h3>
        <p>Valor para ${days} dia(s) e ${adults} adulto(s): <strong>R$${total.toFixed(2)}</strong></p>
    `;
}
</script>