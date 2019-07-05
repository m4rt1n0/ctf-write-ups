# dongdong

- Desafio da etapa de Goiânia do Hackaflag 2019
- Data do desafio: 2019-06-01
- Categoria: rev
- Arquivo fornecido: `dongdong.exe`

## Solução

Inspecionando o arquivo, identificamos que se trata de um executável feito em .NET. O comando `file dongdong.exe`, por exemplo, retorna:

```
dongdong.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```

Um programa útil para descompilar programas em .NET é o [dotPeek](https://www.jetbrains.com/decompiler/) (para Windows) da JetBrains. No dotPeek, podemos encontrar o `Form1.cs` com o seguinte código:

```csharp
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;

namespace dongdong
{
  [DesignerGenerated]
  public class Form1 : Form
  {
    private IContainer components;

    public Form1()
    {
      this.Load += new EventHandler(this.Form1_Load);
      this.InitializeComponent();
    }

    private void Form1_Load(object sender, EventArgs e)
    {
    }

    public static string secret(string data, string key)
    {
      int length1 = data.Length;
      int length2 = key.Length;
      char[] chArray = new char[checked (length1 - 1 + 1)];
      int num = checked (length1 - 1);
      int index = 0;
      while (index <= num)
      {
        chArray[index] = Strings.ChrW(Strings.Asc(data[index]) ^ Strings.Asc(key[index % length2]));
        checked { ++index; }
      }
      return new string(chArray);
    }

    private void Button1_Click(object sender, EventArgs e)
    {
      int num = (int) Interaction.MsgBox((object) "função desativada :(", (MsgBoxStyle) Conversions.ToInteger("1"), (object) "secret");
    }

    [DebuggerNonUserCode]
    protected override void Dispose(bool disposing)
    {
      try
      {
        if (!disposing || this.components == null)
          return;
        this.components.Dispose();
      }
      finally
      {
        base.Dispose(disposing);
      }
    }

    [DebuggerStepThrough]
    private void InitializeComponent()
    {
      this.Button1 = new Button();
      this.TextBox1 = new TextBox();
      this.SuspendLayout();
      this.Button1.Location = new Point(13, 39);
      this.Button1.Name = "Button1";
      this.Button1.Size = new Size(294, 23);
      this.Button1.TabIndex = 0;
      this.Button1.Text = "decode";
      this.Button1.UseVisualStyleBackColor = true;
      this.TextBox1.Location = new Point(13, 13);
      this.TextBox1.Name = "TextBox1";
      this.TextBox1.Size = new Size(294, 20);
      this.TextBox1.TabIndex = 1;
      this.TextBox1.Text = ";$ 9$2?$$\t\x0001\x001B\x001D\x0002\a\x001D\v\x0013\x0014\n\x001B\x001D\x0017\t";
      this.AutoScaleDimensions = new SizeF(6f, 13f);
      this.AutoScaleMode = AutoScaleMode.Font;
      this.ClientSize = new Size(318, 73);
      this.Controls.Add((Control) this.TextBox1);
      this.Controls.Add((Control) this.Button1);
      this.Name = nameof (Form1);
      this.StartPosition = FormStartPosition.CenterScreen;
      this.Text = "Easy cipher";
      this.ResumeLayout(false);
      this.PerformLayout();
    }

    internal virtual Button Button1
    {
      get
      {
        return this._Button1;
      }
      [MethodImpl(MethodImplOptions.Synchronized)] set
      {
        EventHandler eventHandler = new EventHandler(this.Button1_Click);
        Button button1_1 = this._Button1;
        if (button1_1 != null)
          button1_1.Click -= eventHandler;
        this._Button1 = value;
        Button button1_2 = this._Button1;
        if (button1_2 == null)
          return;
        button1_2.Click += eventHandler;
      }
    }

    internal virtual TextBox TextBox1 { get; [MethodImpl(MethodImplOptions.Synchronized)] set; }
  }
}
```

Neste código, a função `secret` chama a atenção. Ela recebe uma string a ser cifrada (`data`), uma chave (`key`) e realiza a operação binária XOR (`^`) entre os caracteres, posição a posição. Se `data` for maior que `key`, o processo continua a partir do primeiro caractere de `key`. Esta é uma [cifra XOR](https://en.wikipedia.org/wiki/XOR_cipher) simples.

Também há uma string suspeita no código: `this.TextBox1.Text = ";$ 9$2?$$\t\x0001\x001B\x001D\x0002\a\x001D\v\x0013\x0014\n\x001B\x001D\x0017\t";`. Supondo que seja a flag e conhecendo o formato `HACKAFLAG{flag}`, podemos realizar um [ataque de texto claro conhecido](https://en.wikipedia.org/wiki/Known-plaintext_attack) para obter a chave e decifrar a string inteira. Para os 10 primeiros caracteres, obtemos:

```
';' ^ 'H' = 's'
'$' ^ 'A' = 'e'
' ' ^ 'C' = 'c'
'9' ^ 'K' = 'r'
'$' ^ 'A' = 'e'
'2' ^ 'F' = 't'
'?' ^ 'L' = 's'
'$' ^ 'A' = 'e'
'$' ^ 'G' = 'c'
'\t' ^ '{' = 'r'
```

Coincidentemente, a operação `'$' ^ 'A' = 'e'` ocorreu três vezes, indicando que estamos no caminho certo. A chave parece ser `secret`, que começa a se repetir no sétimo caractere. Bastam algumas linhas de Python para testar esta hipótese:

```python
data = ';$ 9$2?$$\t\x01\x1B\x1D\x02\a\x1D\v\x13\x14\n\x1B\x1D\x17\t'
secret = 'secret'
cleartext = ''

for i in range(0, len(data)):
	cleartext += chr(ord(data[i]) ^ ord(secret[i%6]))

print(cleartext)
```

O script nos dá a flag `HACKAFLAG{dongdonggoxor}`.