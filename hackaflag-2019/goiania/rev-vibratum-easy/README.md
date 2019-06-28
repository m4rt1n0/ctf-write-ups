# Vibratum_easy

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: rev
- Arquivo fornecido: `app.apk`

## Análise de APK

Um arquivo APK é basicamente um arquivo ZIP renomeado e pode ser extraído com algum programa compatível (com o unzip, por exemplo: `unzip app.apk -d app`). Entre os arquivos extraídos, temos o `classes.dex`, que contém o código das classes Java compiladas para o formato executável do Dalvik (**D**alvik **ex**ecutable), a máquina virtual do Android.

Para descompilar o arquivo `.dex`, podemos utilizar o programa [`dex2jar`](https://github.com/pxb1988/dex2jar). Com o comando `d2j-dex2jar.sh classes.dex`, obtemos o arquivo `classes-dex2jar.jar`. Este, por sua vez, pode ser inspecionado com o programa [JD-GUI](https://github.com/java-decompiler/jd-gui). No pacote `com.hackaflag.chall.vibratum`, encontrando a classe `MainActivity.class` com o seguinte conteúdo:

```
package com.hackaflag.chall.vibratum;

import android.os.Bundle;
import android.os.Vibrator;
import android.support.v7.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
  protected void onCreate(Bundle paramBundle) {
    super.onCreate(paramBundle);
    setContentView(2131296284);
    ((Vibrator)getSystemService("vibrator")).vibrate(new long[] { 
          0L, 200L, 300L, 200L, 200L, 300L, 200L, 200L, 200L, 200L, 
          300L, 200L, 200L, 200L, 200L, 200L, 300L, 200L, 300L, 200L, 
          200L, 200L, 200L, 300L, 300L, 200L, 300L, 200L, 200L, 300L, 
          200L, 300L, 300L, 200L, 300L, 200L, 200L, 200L, 200L, 200L, 
          300L, 200L, 300L, 200L, 200L, 200L, 300L, 300L, 200L, 200L, 
          300L, 200L, 200L, 300L, 300L, 200L, 200L, 200L, 300L, 200L, 
          200L, 200L, 200L, 200L, 300L, 200L, 300L, 200L, 200L, 200L, 
          300L, 300L, 300L, 200L, 300L, 300L, 300L, 300L, 200L, 300L, 
          300L, 200L, 300L, 300L, 200L, 200L, 200L, 300L, 200L, 200L, 
          300L, 300L, 200L, 300L, 200L, 200L, 300L, 200L, 300L, 300L, 
          200L, 300L, 300L, 300L, 200L, 200L, 300L, 300L, 300L, 200L, 
          300L, 200L, 200L, 200L, 300L, 300L, 200L, 300L, 300L, 300L, 
          300L, 200L, 300L, 300L, 300L, 200L, 300L, 200L, 200L, 200L, 
          300L, 300L, 200L, 200L, 300L, 200L, 300L, 200L, 300L, 300L, 
          300L, 300L, 200L, 200L, 200L, 200L, 300L, 300L, 300L, 200L, 
          300L, 200L, 200L, 200L, 300L, 300L, 200L, 200L, 200L, 200L, 
          300L, 200L, 300L, 300L, 200L, 300L, 300L, 300L, 200L, 200L, 
          300L, 300L, 200L, 200L, 300L, 200L, 200L, 200L, 300L, 300L, 
          300L, 200L, 200L, 300L, 200L, 200L, 300L, 300L, 200L, 300L, 
          300L, 300L, 300L, 200L, 300L, 300L, 200L, 300L, 200L, 200L, 
          300L, 200L, 300L, 300L, 200L, 200L, 300L, 200L, 200L, 200L, 
          300L, 300L, 300L, 200L, 300L, 300L, 200L, 200L, 300L, 300L, 
          200L, 300L, 200L, 200L, 300L, 200L, 300L, 300L, 200L, 200L, 
          200L, 300L, 200L, 200L, 300L, 300L, 300L, 200L, 200L, 300L, 
          200L, 200L, 300L, 300L, 200L, 200L, 200L, 200L, 300L, 200L, 
          300L, 300L, 300L, 200L, 300L, 200L, 200L, 200L, 300L, 300L, 
          300L, 200L, 300L, 200L, 300L, 200L, 300L, 300L, 200L, 300L, 
          300L, 200L, 300L, 200L, 300L, 300L, 300L, 300L, 300L, 200L, 
          300L }, 1);
  }
}

```

Este código ativa a vibração do celular e parece conter alguma mensagem. Substituindo `200` por `0` e `300` por `1`, obtemos a sequência

```
0100100001000001010000110100101101000001010001100100110001000001010001110111101101100010011010010110111001110100011011110111010001100101011110000111010001100001011011100110010001110010011011110110100101100100011101100110100101100010011100100110000101110100011101010110110101111101
```

O enunciado ("nem toda vibração é morse") e o fato de haver 280 bits (múltiplo de 8) indicam que estes bits representam uma string. Ao converter de bits para texto, obtemos a flag `HACKAFLAG{bintotextandroidvibratum}`.
