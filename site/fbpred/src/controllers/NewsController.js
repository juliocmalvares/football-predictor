import New from "../models/News";
import { Collection } from 'mongoose';

class NewsController {

    async update(req, res) {
        const { id_new } = req.params;

        const show_new = await New.findOne({ id: id_new });
        const type_req = req.url.split('/')[1];
        console.log(type_req);

        if(show_new.ratings === 3){
            return res.redirect('/');
        }
        if (String(type_req) === "positiva") {
            if (show_new.ratings === 0) {
                show_new.avaliations.aval_1 = "positiva";
            }
            if (show_new.ratings === 1) {
                show_new.avaliations.aval_2 = "positiva";
            }
            if (show_new.ratings === 2) {
                show_new.avaliations.aval_3 = "positiva";
            }
        }

        if (String(type_req) === "negativa") {
            if (show_new.ratings === 0) {
                show_new.avaliations.aval_1 = "negativa";
            }
            if (show_new.ratings === 1) {
                show_new.avaliations.aval_2 = "negativa";
            }
            if (show_new.ratings === 2) {
                show_new.avaliations.aval_3 = "negativa";
            }
        }

        if (String(type_req) === "neutra") {
            if (show_new.ratings === 0) {
                show_new.avaliations.aval_1 = "neutra";
            }
            if (show_new.ratings === 1) {
                show_new.avaliations.aval_2 = "neutra";
            }
            if (show_new.ratings === 2) {
                show_new.avaliations.aval_3 = "neutra";
            }
        }

        if (String(type_req) === "nfutebol") {
            if (show_new.ratings === 0) {
                show_new.avaliations.aval_1 = "nfutebol";
            }
            if (show_new.ratings === 1) {
                show_new.avaliations.aval_2 = "nfutebol";
            }
            if (show_new.ratings === 2) {
                show_new.avaliations.aval_3 = "nfutebol";
            }
        }

        show_new.ratings += 1;
        console.log(id_new);


        await New.updateOne({ id: id_new }, show_new);

        return res.redirect('/');
    }


    async index(req, res) {
        const id_new = 0 + Math.floor((19737) * Math.random());
        const show_new = await New.findOne({ id: String(id_new) });
        let flag = false;
        while (!flag) {
            if (show_new.ratings < 3) {
                flag = true;
            } else {
                show_new = await New.findOne({ id: String(id_new) });
            }
        }


        return res.render("../views/index", { show_new });
    }
}

export default new NewsController();


// {
//     "id": "12922",
//     "time": "gremio",
//     "date": " 28/12/2018 11h44 ",
//     "title": "De herói da Copa do Brasil ao milagre de Guayaquil: reveja cinco defesas de Grohe pelo Grêmio Jogador foi vendido ao Al-Ittihad, da Árabia Saudita, e deixa o Grêmio após 19 temporadas ",
//     "author": "GloboEsporte.com",
//     "text": " Após 19 anos no Grêmio, o goleiro está de. E vai deixar saudades na Arena. Apelidado de \"MilaGrohe\" pela torcida gremista, o camisa 1 teve papel fundamental na série de conquista recentes do Tricolor, sobretudo na Libertadores de 2017, na qual protagonizou o lance que foi considerado a. O lance diante do Barcelona de Guayaquil, aliás, é a favorito do goleiro, que elegeu suas cinco melhores defesas com a camisa do Grêmio no ano passado, a pedido do GloboEsporte.com. Confira a lista abaixo e reveja os lances no vídeo acima. O Grêmio vencia o jogo por 2 a 0 no Equador, quando, aos dois minutos do segundo tempo, o cruzamento vem da direita. Damián Díaz toca de cabeça e Ariel chuta com força, a cerca de dois metros do goleiro. Marcelo se estica e defende com o punho direito. Confronto de ida da final da Copa do Brasil de 2016. Aos 42 do primeiro tempo, enquanto o Grêmio vencia por 1 a 0 no Mineirão, Cazares cruza na área e Júnior Urso finaliza em cima de Marcelo após dominar. O goleiro espalma pela linha de fundo. O Grêmio ganhou o primeiro jogo no Paraná por 1 a 0 e perdeu pelo mesmo placar na Arena, com falha de Marcelo. Nos pênaltis, porém, o goleiro defendeu três cobranças. Ao parar Weverton, Grohe impediu a eliminação gremista. Depois de virar herói, ele chorou e admitiu que poderia ter saído do clube pelas vaias que ouviu da torcida. Aos 25 do primeiro tempo, Bruno cruza na medida para Fred, que manda de cabeça. A bola quica, e Marcelo Grohe voa para salvar o Grêmio. A defesa foi comparada à de Gordon Banks na Copa de 1970, diante de Pelé. Aos 11 do segundo tempo, o placar apontava 0 a 0 na Argentina quando Ponce cabeceou após cobrança de falta do lado direito, Grohe desviou, a bola bateu no travessão e perto da linha, até o goleiro agarrar firme. O atacante chegou a comemorar o gol. ",
//     "url": "https://globoesporte.globo.com/rs/futebol/times/gremio/noticia/de-heroi-da-copa-do-brasil-ao-milagre-de-guayaquil-reveja-cinco-defesas-de-grohe-pelo-gremio.ghtml",
//     "ratings": 0,
//     "avaliations": {
//         "0": "",
//         "1": "",
//         "2": ""
//     }
// }