// Máscara de CPF: 000.000.000-00
function maskCPF(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.substring(0, 11);
    
    if (value.length > 9) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (value.length > 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})/, '$1.$2.$3');
    } else if (value.length > 3) {
        value = value.replace(/(\d{3})(\d{3})/, '$1.$2');
    }
    
    input.value = value;
}

// Máscara de Data: 00/00/0000
function maskData(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.substring(0, 8);
    
    if (value.length > 4) {
        value = value.replace(/(\d{2})(\d{2})(\d{4})/, '$1/$2/$3');
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{2})/, '$1/$2');
    }
    
    input.value = value;
}

// Máscara de Telefone: (00) 0 0000-0000 ou (00) 0000-0000
function maskTelefone(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.substring(0, 11);
    
    if (value.length > 10) {
        value = value.replace(/(\d{2})(\d{1})(\d{4})(\d{4})/, '($1) $2 $3-$4');
    } else if (value.length > 6) {
        value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    } else if (value.length > 0) {
        value = value.replace(/(\d{0,2})/, '($1');
    }
    
    input.value = value;
}

// Máscara de DDD: 00
function maskDDD(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.substring(0, 2);
    input.value = value;
}

// Máscara de CEP: 00000-000
function maskCEP(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.substring(0, 8);
    
    if (value.length > 5) {
        value = value.replace(/(\d{5})(\d{3})/, '$1-$2');
    }
    
    input.value = value;
}

// Autocomplete de domínios de e-mail
const emailDomains = [
    'gmail.com',
    'hotmail.com',
    'outlook.com',
    'yahoo.com.br',
    'yahoo.com',
    'icloud.com',
    'live.com',
    'uol.com.br',
    'terra.com.br',
    'bol.com.br',
    'ig.com.br',
    'globo.com',
    'me.com'
];

function setupEmailAutocomplete(input) {
    const datalistId = input.id + '-domains';
    let datalist = document.getElementById(datalistId);
    
    if (!datalist) {
        datalist = document.createElement('datalist');
        datalist.id = datalistId;
        input.setAttribute('list', datalistId);
        input.parentNode.appendChild(datalist);
    }
    
    input.addEventListener('input', function() {
        const value = this.value;
        const atIndex = value.indexOf('@');
        
        datalist.innerHTML = '';
        
        if (atIndex !== -1) {
            const username = value.substring(0, atIndex);
            const domain = value.substring(atIndex + 1);
            
            emailDomains.forEach(function(emailDomain) {
                if (emailDomain.startsWith(domain) || domain === '') {
                    const option = document.createElement('option');
                    option.value = username + '@' + emailDomain;
                    datalist.appendChild(option);
                }
            });
        }
    });
}

// Consultar CEP na API ViaCEP
function consultarCEP(cep) {
    const cepLimpo = cep.replace(/\D/g, '');
    
    if (cepLimpo.length === 8) {
        fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    const logradouroInput = document.getElementById('logradouro');
                    const bairroInput = document.getElementById('bairro');
                    const cidadeInput = document.getElementById('cidade_endereco');
                    const ufSelect = document.getElementById('uf_endereco');
                    
                    if (logradouroInput && data.logradouro) {
                        logradouroInput.value = data.logradouro;
                    }
                    
                    if (bairroInput && data.bairro) {
                        bairroInput.value = data.bairro;
                    }
                    
                    if (cidadeInput && data.localidade) {
                        cidadeInput.value = data.localidade;
                    }
                    
                    if (ufSelect && data.uf) {
                        ufSelect.value = data.uf;
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao consultar CEP:', error);
            });
    }
}

// Aplicar máscaras quando o documento carregar
document.addEventListener('DOMContentLoaded', function() {
    // CPF
    const cpfInputs = document.querySelectorAll('input[name="cpf"], input[name="cpf_responsavel"]');
    cpfInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            maskCPF(this);
        });
    });
    
    // Data de nascimento
    const dataInputs = document.querySelectorAll('input[name="data_nascimento"], input[name="data_emissao"], input[name="data_expedicao"]');
    dataInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            maskData(this);
        });
    });
    
    // Telefone
    const telefoneInputs = document.querySelectorAll('input[name="telefone"]');
    telefoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            maskTelefone(this);
        });
    });
    
    // CEP com máscara e consulta automática
    const cepInputs = document.querySelectorAll('input[name="cep"]');
    cepInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            maskCEP(this);
            consultarCEP(this.value);
        });
    });
    
    // E-mail autocomplete
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(function(input) {
        setupEmailAutocomplete(input);
    });
});
