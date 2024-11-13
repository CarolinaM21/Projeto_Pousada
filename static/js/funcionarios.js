// Abrir o modal para adicionar ou editar um funcionário
function adicionarFuncionario() {
    document.getElementById("modal-title").innerText = "Adicionar Funcionário";
    document.getElementById("form-funcionario").reset();
    document.getElementById("funcionario-id").value = "";
    document.getElementById("modal").style.display = "block";
}

function editarFuncionario(id) {
    // Pegar dados do funcionário pelo ID e preencher o formulário
    fetch(`/get_funcionario/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("modal-title").innerText = "Editar Funcionário";
            document.getElementById("funcionario-id").value = data.id;
            document.getElementById("nome").value = data.nome;
            document.getElementById("cargo").value = data.cargo;
            document.getElementById("horario_trabalho").value = data.horario_trabalho;
            document.getElementById("status").value = data.status;
            document.getElementById("modal").style.display = "block";
        });
}

// Fechar o modal
function fecharModal() {
    document.getElementById("modal").style.display = "none";
}

// Salvar funcionário (adicionar ou atualizar)
function salvarFuncionario() {
    const id = document.getElementById("funcionario-id").value;
    const nome = document.getElementById("nome").value;
    const cargo = document.getElementById("cargo").value;
    const horario_trabalho = document.getElementById("horario_trabalho").value;
    const status = document.getElementById("status").value;

    const url = id ? `/editar_funcionario/${id}` : '/adicionar_funcionario';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, cargo, horario_trabalho, status })
    })
    .then(response => {
        if (response.ok) {
            alert("Funcionário salvo com sucesso!");
            window.location.reload();
        } else {
            alert("Erro ao salvar o funcionário.");
        }
    });
}

// Excluir funcionário
function excluirFuncionario(id) {
    if (confirm("Tem certeza de que deseja excluir este funcionário?")) {
        fetch(`/excluir_funcionario/${id}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    alert("Funcionário excluído com sucesso!");
                    window.location.reload();
                } else {
                    alert("Erro ao excluir o funcionário.");
                }
            });
    }
}
