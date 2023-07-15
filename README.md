Main.py - Chama a API do google (substituir credenciais) para o treinamento de speech (detecção de fala) e salva os resultados para um json no blog (substituir caminhos no código também)

check_files.py- Verifica todos Json  que foram criados no blob, e faz o download na pasta escolhida(substituir no código)

parsing_bytes.py- Formata o JSON para o formato que o site algolia que é nossa API de pesquisa precisa, apenas colocar diretorio de entrada e um de saída e ele faz o trabalho

algolia_test.py - manda o JSON para algolia, caso algum falhe ele mostra no console no final da execução

website.py - APP Flask que roda nossa search Engine
Front-end Simples porque sou preguiçoso e precisava que funcionasse.

Tirei a ideia desse artigo - https://daleonai.com/building-an-ai-powered-searchable-video-archive

Antes de tudo instale e faça a verificação do gcloud CLI
https://cloud.google.com/sdk/gcloud

Pesquisa:
<img width="575" alt="CleanShot 2023-07-15 at 19 15 47@2x" src="https://github.com/lucasfersilva/ai-video-search/assets/37738836/ef51a95b-4310-4ab9-9cbf-7eb4270bbc56">

￼

Resultados:
<img width="584" alt="CleanShot 2023-07-15 at 19 15 28@2x" src="https://github.com/lucasfersilva/ai-video-search/assets/37738836/065277ef-e918-4f2c-92ee-302bcd0db9f3">

￼


