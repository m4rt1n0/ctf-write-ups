# nofite

- Desafio da etapa de Belo Horizonte do Hackaflag 2019
- Data do desafio: 29-06-2019
- Categoria: forense
- Arquivos fornecidos: `for01.zip`

A descrição do desafio informa que a flag está no formato `HACKAFLAG{senha-bssid}`. Abrindo o arquivo `for01.zip`, encontramos dois arquivos: `hackaflag-01.cap` e `hackaflag-02.cap`.

Arquivos `.cap` armazenam capturas de pacotes de rede e podem ser abertos com o [Wireshark](https://www.wireshark.org/). Inspecionando os arquivos com o Wireshark, encontramos alguns dispositivos se conectando a uma rede sem fio chamada HACKAFLAG, cujo BSSID (_Basic Service Set Identifier_) é `70:4F:57:07:4B:6E`. Aqui, já temos o BSSID necessário para a flag, mas precisamos descobrir a senha desta rede.

Durante o processo de autenticação em uma rede sem fio WPA/WPA2 com PSK (_Pre-shared Key_, chave pré-compartilhada), ocorre o que se chama de _four-way handshake_ (aperto de mãos de quatro vias), no qual o ponto de acesso (_access point_ ou AP) e o cliente provam um ao outro que conhecem a PSK, mas sem revelá-la. Se as informações trocadas neste processo forem capturadas, é possível tentar encontrar a senha utilizando o [aircrack-ng](https://www.aircrack-ng.org/).

Para encontrar a senha de uma rede WPA/WPA2, um ataque de força bruta é inviável. As redes possuem um tamanho mínimo de chave de 8 caracteres. Assumindo que uma rede tenha uma senha de apenas 8 caracteres minúsculos, isso resulta em 26<sup>8</sup> = 208827064576 possibilidades. Testando 3000 chaves por segundo, seriam necessários aproximadamente 805 dias para testar todas as possibilidades.

Um ataque de dicionário é mais eficiente para encontrar senhas com padrões mais humanos e menos aleatórios (e é por isso que senhas aleatórias são mais seguras). Um dos dicionários mais comuns é o `rockyou.txt` (que já vem na instalação do Kali Linux). Vamos executar o `aircrack-ng` informando o dicionário com a opção `-w`.

```
aircrack-ng -w rockyou.txt *.cap
```

Em alguns minutos encontramos a senha da rede:

```
                                 Aircrack-ng 1.2 rc4

      [00:20:26] 3621896/9822769 keys tested (3014.77 k/s)

      Time left: 34 minutes, 17 seconds                         36.87%

                         KEY FOUND! [ mary21juanpa ]


      Master Key     : 81 DA 0F 2F 18 86 AD 68 43 76 75 5A D3 93 90 9B
                       08 2C 83 4F 55 1C FE 26 BE E3 36 1F B6 A8 A1 AA

      Transient Key  : CC 09 4C 0E B2 82 24 8B A8 11 35 0C F2 4E 9F 2B
                       C8 97 CB 07 54 67 01 E2 C8 8F F5 DB F4 A0 29 4A
                       24 82 48 C7 3D 54 87 04 FB DD 94 E6 9B 64 F6 18
                       83 C0 D8 83 A3 0B AB 62 A9 0B 88 4F 5A 8F EA 8B

      EAPOL HMAC     : 3B 53 2F 7F 97 E2 D3 22 54 54 65 82 C1 49 C2 B8
```

Assim, a flag é `HACKAFLAG{mary21juanpa-70:4F:57:07:4B:6E}`.
