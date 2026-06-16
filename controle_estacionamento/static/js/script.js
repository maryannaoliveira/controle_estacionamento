// RELÓGIO

function atualizarRelogio(){

    const agora = new Date()
    const hora = agora.toLocaleTimeString('pt-BR')
    const relogio =
    document.getElementById('relogio')

    if(relogio){
        relogio.innerHTML = hora}
}
setInterval(
    atualizarRelogio,1000)
atualizarRelogio()

const cards =
document.querySelectorAll('.card-dashboard')
cards.forEach(card => {
    card.addEventListener('mouseenter',
        () => {
            card.style.boxShadow =
            '0px 0px 25px rgba(59,130,246,0.5)'
        }
    )

    card.addEventListener(
        'mouseleave',
        () => {
            card.style.boxShadow =
            'none'
        }
    )
})

function tocarSomAlerta(){

    try{

        const audioCtx =
        new (window.AudioContext || window.webkitAudioContext)()

        const oscillator =
        audioCtx.createOscillator()

        const gainNode =
        audioCtx.createGain()

        oscillator.connect(
            gainNode
        )

        gainNode.connect(
            audioCtx.destination
        )

        oscillator.type = 'sine'

        oscillator.frequency.setValueAtTime(
            880,
            audioCtx.currentTime
        )

        gainNode.gain.setValueAtTime(
            0.1,
            audioCtx.currentTime
        )

        oscillator.start()

        oscillator.stop(
            audioCtx.currentTime + 0.15
        )

    }catch(e){

        console.log(
            'Som bloqueado pelo navegador.'
        )
    }
}

let alternarTitulo = false
let tituloOriginal =
document.title

function checarTemposERecados(){

    const linhas =
    document.querySelectorAll(
        '.linha-veiculo'
    )

    let existemAtrasados =
    false

    linhas.forEach(linha => {

        const entradaTexto =
        linha.dataset.entrada

        if(!entradaTexto){

            return
        }

        const entrada =
        new Date(
            entradaTexto.replace(
                ' ',
                'T'
            )
        )

        const agora =
        new Date()

        const tempoAtual =
        Math.floor(
            (agora - entrada) / 60000
        )

        const campoStatus =
        linha.querySelector(
            '.status'
        )

        const campoValor =
        linha.querySelector(
            '.valor-tempo-real'
        )

        const campoAviso =
        linha.querySelector(
            '.aviso-excesso'
        )

        let valorAtual = 0

        if(tempoAtual <= 15){

            linha.classList.remove(
                'alerta'
            )

            if(campoStatus){

                campoStatus.innerText =
                '✅ Gratuito'

                campoStatus.className =
                'status badge bg-success'

            }

            if(campoAviso){

                campoAviso.style.display =
                'none'

            }

        }

        else{

            valorAtual = 10
            if(tempoAtual > 60){
                const tempoExtra =
                tempoAtual - 60

                const blocosExtras =
                Math.ceil(
                    tempoExtra / 15
                )

                valorAtual +=
                blocosExtras * 3

            }

            existemAtrasados =
            true

            linha.classList.add(
                'alerta'
            )

            if(campoStatus){

                campoStatus.innerText =
                '⚠️ Tempo Excedido'

                campoStatus.className =
                'status badge bg-danger fw-bold'

            }

            if(campoAviso){

                campoAviso.innerText =
                `Valor Atual: R$ ${valorAtual.toFixed(2)}`

                campoAviso.style.display =
                'inline-block'

            }

        }


        if(campoValor){

            campoValor.innerText =
            `R$ ${valorAtual.toFixed(2)}`

        }

    })


    if(existemAtrasados){

        tocarSomAlerta()

        alternarTitulo =
        !alternarTitulo

        document.title =
        alternarTitulo
        ? '🚨 TEMPO EXCEDIDO!'
        : '⚠️ VERIFICAR PÁTIO'

    }

    else{

        document.title =
        tituloOriginal

    }

}


setInterval(
    checarTemposERecados,
    1000
)

checarTemposERecados()

