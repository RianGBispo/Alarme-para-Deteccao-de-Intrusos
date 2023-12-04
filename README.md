
<h1>🚨 Projeto de Detecção de Invasores: Reforçando a Segurança com Python! 🚨</h1>

<p>Este é um projeto de vigilância utilizando detecção de objetos para identificar intrusos em uma cena de vídeo. O código é escrito em Python e utiliza as seguintes bibliotecas e ferramentas:</p>

<h2>Requisitos</h2>
<ul>
  <li>Python</li>
  <li>OpenCV</li>
  <li>NumPy</li>
  <li>Pygame</li>
  <li>win32com.client (para envio de e-mails no Windows)</li>
  <li>Power BI (opcional, para visualização dos dados)</li>
</ul>
<h2>Estrutura do Projeto</h2>
<ul>
  <li><strong>Detecção de Movimento:</strong> Utiliza a técnica de subtração de fundo para detectar áreas em movimento na cena.</li>
  <li><strong>Detecção de Intrusos:</strong> Identifica intrusos na cena após um determinado número de frames, desenhando caixas delimitadoras ao redor de áreas em movimento significativas.</li>
  <li><strong>Alarme e Notificação por E-mail:</strong> Aciona um alarme sonoro e envia um e-mail com uma imagem do momento da detecção.</li>
</ul>
<h2>Configuração</h2>
<p>Antes de executar o projeto, certifique-se de ajustar as seguintes configurações no arquivo <code>main.py</code>:</p>
<ul>
  <li><code>video_source</code>: Caminho do vídeo ou dispositivo de entrada.</li>
  <li><code>FRAME_START</code>: Número de frames antes do início da detecção.</li>
  <li>Configurações de texto e fonte para rótulos e alertas.</li>
</ul>
<h2>Uso</h2>
<p>Execute o script <code>main.py</code> para iniciar a vigilância. A janela exibirá a transmissão da câmera com caixas delimitadoras ao redor de intrusos detectados.</p>
<h2>Dependências</h2>
<p>Certifique-se de ter as dependências instaladas. Você pode instalá-las usando o seguinte comando:</p>
<pre><code>pip install opencv-python numpy pygame</code></pre>
<h2>Observações</h2>
<ul>
  <li>O script foi configurado para utilizar o Outlook para envio de e-mails. Ajuste a função <code>send_email</code> de acordo com suas preferências de e-mail.</li>
  <li>Certifique-se de ter o arquivo de som do alarme (<code>data/alarm.wav</code>) na pasta correta.</li>
  <li>Este projeto é um ponto de partida e pode ser expandido para incluir mais recursos, como detecção de múltiplos objetos, integração com APIs de serviços de nuvem, entre outros.</li>
</ul>
<p>Lembre-se de ajustar e personalizar o projeto conforme suas necessidades específicas. Boa sorte com seu projeto de vigilância!</p>
<h2>Fontes</h2>
<ul>
  <li>Documentação do OpenCV: <a href="https://docs.opencv.org/">OpenCV Documentation</a></li>
  <li>Documentação do Pygame: <a href="https://www.pygame.org/docs/">Pygame Documentation</a></li>
</ul>
