# Bloco de Reflexão — Lab 04

## 1) Síntese
Para mim, o tipo de transparência mais difícil de acertar é a de falha, e a Tarefa 7 mostrou bem o porquê. Não adianta só tentar "esconder" que a rede deu erro; o sistema precisa saber como degradar de forma controlada para não travar tudo. Para isso funcionar na prática, a gente precisa combinar conceitos como timeout, retry e circuit breaker, além de garantir a idempotência das operações. Em um cenário real, cada serviço falha de um jeito, e sem uma boa observabilidade, é impossível criar políticas de resiliência que realmente funcionem.

## 2) Trade-offs
Um exemplo clássico de trade-off é o que acontece em apps de transporte. Se a gente tentar esconder totalmente a distribuição, acaba mascarando latências que o usuário precisaria conhecer. Se o app fingir que tudo é local e instantâneo, o usuário fica perdido quando o preço ou o mapa não atualizam. Mostrar o estado da conexão ou avisar que está "tentando reconectar" acaba sendo uma decisão de design melhor, porque evita a falácia de que "a rede é confiável" e deixa claro que o sistema trabalha com consistência eventual.

## 3) Conexão com Labs anteriores
O uso do `async/await` que vimos no Lab 02 faz todo sentido quando chegamos na transparência consciente da Tarefa 7. Quando a gente define uma função como assíncrona, o próprio código já avisa que ali existe uma espera que a gente não controla (I/O remoto). Isso quebra um pouco aquela ilusão de que a chamada é local, mas por outro lado melhora muito o projeto, porque obriga o desenvolvedor a pensar logo de cara em como tratar timeouts, cancelamentos e a latência da rede.

## 4) GIL e multiprocessing
Na Tarefa 6, usamos o `multiprocessing` justamente porque cada processo roda de forma independente no sistema operacional, com sua própria memória. Isso é bem diferente de usar threads no CPython, onde o GIL (Global Interpreter Lock) acaba serializando a execução do bytecode e pode "esconder" algumas race conditions durante os testes. Usando processos separados e um Redis externo, o cenário fica muito mais próximo de um sistema distribuído de verdade, o que deixa clara a importância de usar um lock distribuído para não corromper os dados.

## 5) Desafio técnico
O que mais deu trabalho nesse laboratório foi o setup inicial da conexão com o Redis Cloud. O diagnóstico demorou um pouco, mas resolvi conferindo as credenciais no `.env` e percebendo que, no plano gratuito "Essentials", o `ssl=False` era obrigatório para evitar erros de protocolo. Só depois de criar um script simples de `ping` e `set/get` para validar a conexão é que consegui avançar com segurança para as tarefas de migração e os testes de concorrência, garantindo que os resultados fossem reproduzíveis.