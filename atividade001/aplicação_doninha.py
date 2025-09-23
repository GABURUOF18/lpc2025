import random

title = "CIGS Zoo Interactive (Weasel Evolution Mode)"
print(title)

# ==============================
# Animals List
# ==============================
animals = [
    "Onça-pintada", "Arara-azul", "Tamanduá-bandeira", "Tucano-toco",
    "Lobo-guará", "Mico-leão-dourado", "Capivara", "Jabuti", "Sucuri"
]

# ==============================
# Questions for all animals
# ==============================

questions = [
    # ---- Onça-pintada ----
    {"animal": "Onça-pintada", "question": "Qual é o maior felino das Américas?", "options": ["Onça-pintada", "Puma", "Jaguatirica", "Gato-do-mato"], "correct": 0, "difficulty": "easy"},
    {"animal": "Onça-pintada", "question": "Onde a onça-pintada costuma viver?", "options": ["Florestas tropicais", "Desertos", "Tundras", "Montanhas nevadas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Onça-pintada", "question": "Qual a cor predominante da pelagem da onça?", "options": ["Amarela com manchas pretas", "Marrom", "Cinza", "Branca"], "correct": 0, "difficulty": "easy"},
    {"animal": "Onça-pintada", "question": "O que distingue a onça-pintada de outros felinos?", "options": ["Rosetas com pontos no centro", "Listras", "Manchas simples", "Pelagem lisa"], "correct": 0, "difficulty": "medium"},
    {"animal": "Onça-pintada", "question": "Qual o peso médio de uma onça adulta?", "options": ["80–120kg", "20–40kg", "200kg", "10kg"], "correct": 0, "difficulty": "medium"},
    {"animal": "Onça-pintada", "question": "Principal habitat no Brasil?", "options": ["Amazônia e Pantanal", "Caatinga", "Pampas", "Litoral"], "correct": 0, "difficulty": "medium"},
    {"animal": "Onça-pintada", "question": "Técnica de caça característica?", "options": ["Mordida no crânio", "Sufocamento", "Quebra do pescoço", "Caça em grupo"], "correct": 0, "difficulty": "hard"},
    {"animal": "Onça-pintada", "question": "A onça é considerada?", "options": ["Predador de topo", "Herbívoro", "Onívoro", "Predador secundário"], "correct": 0, "difficulty": "hard"},
    {"animal": "Onça-pintada", "question": "Principal ameaça à espécie?", "options": ["Desmatamento e caça", "Predadores", "Doenças", "Mudança climática"], "correct": 0, "difficulty": "hard"},
   
    # ---- Arara-azul ----
    {"animal": "Arara-azul", "question": "Qual o nome científico da arara-azul?", "options": ["Anodorhynchus hyacinthinus", "Ara ararauna", "Ara macao", "Cyanopsitta spixii"], "correct": 0, "difficulty": "easy"},
    {"animal": "Arara-azul", "question": "O que a arara-azul come?", "options": ["Cocos de palmeiras", "Insetos", "Pequenos vertebrados", "Folhas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Arara-azul", "question": "Qual o tamanho médio de uma arara-azul?", "options": ["1 metro", "50 cm", "30 cm", "1,5 metros"], "correct": 0, "difficulty": "easy"},
    {"animal": "Arara-azul", "question": "Onde a arara-azul faz seu ninho?", "options": ["Ocos de árvores", "No chão", "Em rochas", "Em arbustos"], "correct": 0, "difficulty": "medium"},
    {"animal": "Arara-azul", "question": "Quantos ovos ela põe por ninhada?", "options": ["1-2 ovos", "3-5 ovos", "5-7 ovos", "8-10 ovos"], "correct": 0, "difficulty": "medium"},
    {"animal": "Arara-azul", "question": "Qual é seu principal habitat?", "options": ["Pantanal e Cerrado", "Amazônia", "Mata Atlântica", "Caatinga"], "correct": 0, "difficulty": "medium"},
    {"animal": "Arara-azul", "question": "Qual é seu status de conservação?", "options": ["Vulnerável", "Extinta", "Pouco preocupante", "Em perigo crítico"], "correct": 0, "difficulty": "hard"},
    {"animal": "Arara-azul", "question": "Qual a principal ameaça à arara-azul?", "options": ["Tráfico e perda de habitat", "Predadores naturais", "Doenças", "Mudanças climáticas"], "correct": 0, "difficulty": "hard"},
    {"animal": "Arara-azul", "question": "Quanto tempo vive uma arara-azul em cativeiro?", "options": ["Até 50 anos", "10 anos", "25 anos", "5 anos"], "correct": 0, "difficulty": "hard"},
   
    # ---- Tamanduá-bandeira ----
    {"animal": "Tamanduá-bandeira", "question": "O que o tamanduá-bandeira come?", "options": ["Formigas e cupins", "Frutas", "Pequenos animais", "Folhas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tamanduá-bandeira", "question": "Qual sua característica física mais marcante?", "options": ["Focinho longo e língua pegajosa", "Cauda longa", "Garras afiadas", "Orelhas grandes"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tamanduá-bandeira", "question": "Onde ele vive?", "options": ["Cerrado e campos", "Desertos", "Florestas densas", "Montanhas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tamanduá-bandeira", "question": "Quantas crias ele tem por gestação?", "options": ["1", "2-3", "4-5", "6-7"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tamanduá-bandeira", "question": "Qual o comprimento de sua língua?", "options": ["Até 60 cm", "10 cm", "30 cm", "1 metro"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tamanduá-bandeira", "question": "Como se defende de predadores?", "options": ["Usa suas garras dianteiras", "Foge rapidamente", "Morde", "Esconde-se"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tamanduá-bandeira", "question": "Qual seu status de conservação?", "options": ["Vulnerável", "Extinto", "Pouco preocupante", "Em perigo crítico"], "correct": 0, "difficulty": "hard"},
    {"animal": "Tamanduá-bandeira", "question": "Quantas formigas pode comer por dia?", "options": ["Até 30.000", "100", "1.000", "5.000"], "correct": 0, "difficulty": "hard"},
    {"animal": "Tamanduá-bandeira", "question": "Qual a principal ameaça ao tamanduá-bandeira?", "options": ["Atropelamentos e incêndios", "Predadores naturais", "Doenças", "Competição por alimento"], "correct": 0, "difficulty": "hard"},
   
    # ---- Tucano-toco ----
    {"animal": "Tucano-toco", "question": "Qual a característica mais marcante do tucano-toco?", "options": ["Bico grande e colorido", "Penas coloridas", "Cauda longa", "Pernas altas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tucano-toco", "question": "O que o tucano-toco come?", "options": ["Frutas, ovos e insetos", "Apenas frutas", "Apenas insetos", "Peixes"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tucano-toco", "question": "Onde vive o tucano-toco?", "options": ["Cerrado e florestas abertas", "Desertos", "Tundras", "Oceanos"], "correct": 0, "difficulty": "easy"},
    {"animal": "Tucano-toco", "question": "Qual o tamanho de seu bico?", "options": ["Cerca de 20 cm", "5 cm", "50 cm", "1 metro"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tucano-toco", "question": "Para que serve seu bico grande?", "options": ["Termorregulação e alimentação", "Defesa apenas", "Natação", "Cavar"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tucano-toco", "question": "Como são seus ninhos?", "options": ["Ocos de árvores", "No chão", "Em rochas", "Arbustos"], "correct": 0, "difficulty": "medium"},
    {"animal": "Tucano-toco", "question": "Quantos ovos põe por ninhada?", "options": ["2-4 ovos", "1 ovo", "5-7 ovos", "8-10 ovos"], "correct": 0, "difficulty": "hard"},
    {"animal": "Tucano-toco", "question": "Qual seu status de conservação?", "options": ["Pouco preocupante", "Em perigo", "Vulnerável", "Extinto"], "correct": 0, "difficulty": "hard"},
    {"animal": "Tucano-toco", "question": "Qual a principal função de suas cores vibrantes?", "options": ["Comunicação e camuflagem", "Atrair presas", "Proteção solar", "Natação"], "correct": 0, "difficulty": "hard"},
   
    # ---- Lobo-guará ----
    {"animal": "Lobo-guará", "question": "O que o lobo-guará come?", "options": ["Frutas e pequenos animais", "Apenas carne", "Apenas frutas", "Peixes"], "correct": 0, "difficulty": "easy"},
    {"animal": "Lobo-guará", "question": "Qual sua característica física mais marcante?", "options": ["Pernas longas e pelagem alaranjada", "Orelhas pontudas", "Cauda curta", "Manchas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Lobo-guará", "question": "Onde vive o lobo-guará?", "options": ["Cerrado", "Amazônia", "Pantanal", "Caatinga"], "correct": 0, "difficulty": "easy"},
    {"animal": "Lobo-guará", "question": "Qual fruta é sua preferida?", "options": ["Lobeira", "Banana", "Manga", "Maçã"], "correct": 0, "difficulty": "medium"},
    {"animal": "Lobo-guará", "question": "Qual seu status de conservação?", "options": ["Quase ameaçado", "Extinto", "Pouco preocupante", "Em perigo crítico"], "correct": 0, "difficulty": "medium"},
    {"animal": "Lobo-guará", "question": "Qual o tamanho médio de um lobo-guará?", "options": ["1 metro de altura", "50 cm", "1,5 metros", "2 metros"], "correct": 0, "difficulty": "medium"},
    {"animal": "Lobo-guará", "question": "Quantos filhotes tem por ninhada?", "options": ["2-3", "1", "4-5", "6-7"], "correct": 0, "difficulty": "hard"},
    {"animal": "Lobo-guará", "question": "Qual a principal ameaça ao lobo-guará?", "options": ["Perda de habitat e atropelamentos", "Predadores", "Doenças", "Competição"], "correct": 0, "difficulty": "hard"},
    {"animal": "Lobo-guará", "question": "Qual o nome científico do lobo-guará?", "options": ["Chrysocyon brachyurus", "Canis lupus", "Lycalopex vetulus", "Cerdocyon thous"], "correct": 0, "difficulty": "hard"},
   
    # ---- Mico-leão-dourado ----
    {"animal": "Mico-leão-dourado", "question": "Qual a cor predominante do mico-leão-dourado?", "options": ["Dourado", "Preto", "Marrom", "Cinza"], "correct": 0, "difficulty": "easy"},
    {"animal": "Mico-leão-dourado", "question": "Onde vive o mico-leão-dourado?", "options": ["Mata Atlântica", "Amazônia", "Cerrado", "Caatinga"], "correct": 0, "difficulty": "easy"},
    {"animal": "Mico-leão-dourado", "question": "O que ele come?", "options": ["Frutas, insetos e pequenos vertebrados", "Apenas frutas", "Apenas insetos", "Folhas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Mico-leão-dourado", "question": "Qual seu status de conservação?", "options": ["Em perigo", "Extinto", "Pouco preocupante", "Vulnerável"], "correct": 0, "difficulty": "medium"},
    {"animal": "Mico-leão-dourado", "question": "Qual o tamanho médio de um mico-leão-dourado?", "options": ["20-30 cm", "50-60 cm", "10-15 cm", "40-50 cm"], "correct": 0, "difficulty": "medium"},
    {"animal": "Mico-leão-dourado", "question": "Quantos filhotes tem por gestação?", "options": ["Geralmente gêmeos", "1", "3-4", "5-6"], "correct": 0, "difficulty": "medium"},
    {"animal": "Mico-leão-dourado", "question": "Qual a principal ameaça ao mico-leão-dourado?", "options": ["Fragmentação florestal", "Predadores", "Doenças", "Competição"], "correct": 0, "difficulty": "hard"},
    {"animal": "Mico-leão-dourado", "question": "Qual o nome científico do mico-leão-dourado?", "options": ["Leontopithecus rosalia", "Callithrix jacchus", "Saguinus oedipus", "Cebus apella"], "correct": 0, "difficulty": "hard"},
    {"animal": "Mico-leão-dourado", "question": "Qual projeto famoso atua na conservação desta espécie?", "options": ["Projeto Mico-Leão-Dourado", "Projeto Tamar", "Projeto Onça-Pintada", "Projeto Arara-Azul"], "correct": 0, "difficulty": "hard"},
   
    # ---- Capivara ----
    {"animal": "Capivara", "question": "Qual o maior roedor do mundo?", "options": ["Capivara", "Paca", "Cutia", "Rato"], "correct": 0, "difficulty": "easy"},
    {"animal": "Capivara", "question": "Onde a capivara vive?", "options": ["Perto de rios e lagos", "Desertos", "Montanhas", "Florestas densas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Capivara", "question": "O que a capivara come?", "options": ["Gramíneas e plantas aquáticas", "Apenas frutas", "Peixes", "Insetos"], "correct": 0, "difficulty": "easy"},
    {"animal": "Capivara", "question": "Qual seu comportamento social?", "options": ["Vive em grupos", "Vive sozinha", "Vive em pares", "Vive em grandes manadas"], "correct": 0, "difficulty": "medium"},
    {"animal": "Capivara", "question": "Qual o peso médio de uma capivara adulta?", "options": ["50-60 kg", "20 kg", "100 kg", "10 kg"], "correct": 0, "difficulty": "medium"},
    {"animal": "Capivara", "question": "Qual a gestação de uma capivara?", "options": ["5 meses", "2 meses", "9 meses", "1 ano"], "correct": 0, "difficulty": "medium"},
    {"animal": "Capivara", "question": "Quantos filhotes tem por ninhada?", "options": ["4-5", "1-2", "6-7", "8-9"], "correct": 0, "difficulty": "hard"},
    {"animal": "Capivara", "question": "Qual o nome científico da capivara?", "options": ["Hydrochoerus hydrochaeris", "Cavia aperea", "Dasyprocta leporina", "Myocastor coypus"], "correct": 0, "difficulty": "hard"},
    {"animal": "Capivara", "question": "Qual predador natural da capivara?", "options": ["Onça-pintada e jacaré", "Tucano", "Tamanduá", "Arara"], "correct": 0, "difficulty": "hard"},
   
    # ---- Jabuti ----
    {"animal": "Jabuti", "question": "O que é um jabuti?", "options": ["Um réptil", "Um anfíbio", "Um mamífero", "Uma ave"], "correct": 0, "difficulty": "easy"},
    {"animal": "Jabuti", "question": "O que o jabuti come?", "options": ["Frutas, verduras e legumes", "Apenas carne", "Apenas insetos", "Peixes"], "correct": 0, "difficulty": "easy"},
    {"animal": "Jabuti", "question": "Onde o jabuti vive?", "options": ["Florestas e cerrados", "Desertos", "Oceanos", "Montanhas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Jabuti", "question": "Qual a diferença entre jabuti e cágado?", "options": ["Jabuti é terrestre, cágado é aquático", "Jabuti é maior", "Cágado tem casco mais alto", "Não há diferença"], "correct": 0, "difficulty": "medium"},
    {"animal": "Jabuti", "question": "Quanto tempo vive um jabuti?", "options": ["Até 80 anos", "10 anos", "30 anos", "5 anos"], "correct": 0, "difficulty": "medium"},
    {"animal": "Jabuti", "question": "Quantos ovos põe por ninhada?", "options": ["5-15 ovos", "1-2 ovos", "20-30 ovos", "50 ovos"], "correct": 0, "difficulty": "medium"},
    {"animal": "Jabuti", "question": "Qual o nome científico do jabuti-piranga?", "options": ["Chelonoidis carbonaria", "Geochelone denticulata", "Testudo graeca", "Trachemys scripta"], "correct": 0, "difficulty": "hard"},
    {"animal": "Jabuti", "question": "Como o jabuti se defende?", "options": ["Recolhendo-se no casco", "Mordendo", "Correndo", "Saltando"], "correct": 0, "difficulty": "hard"},
    {"animal": "Jabuti", "question": "Qual a principal ameaça aos jabutis?", "options": ["Tráfico ilegal e perda de habitat", "Predadores", "Doenças", "Competição"], "correct": 0, "difficulty": "hard"},
   
    # ---- Sucuri ----
    {"animal": "Sucuri", "question": "O que é uma sucuri?", "options": ["Uma cobra constritora", "Uma cobra venenosa", "Um lagarto", "Um anfíbio"], "correct": 0, "difficulty": "easy"},
    {"animal": "Sucuri", "question": "Onde a sucuri vive?", "options": ["Rios e áreas alagadas", "Desertos", "Montanhas", "Florestas secas"], "correct": 0, "difficulty": "easy"},
    {"animal": "Sucuri", "question": "Como a sucuri mata suas presas?", "options": ["Constrição", "Veneno", "Afogamento", "Mordida"], "correct": 0, "difficulty": "easy"},
    {"animal": "Sucuri", "question": "Qual o comprimento médio de uma sucuri adulta?", "options": ["4-6 metros", "2 metros", "10 metros", "1 metro"], "correct": 0, "difficulty": "medium"},
    {"animal": "Sucuri", "question": "O que a sucuri come?", "options": ["Peixes, aves e mamíferos", "Apenas peixes", "Apenas insetos", "Plantas"], "correct": 0, "difficulty": "medium"},
    {"animal": "Sucuri", "question": "Qual a diferença entre sucuri e anaconda?", "options": ["São nomes diferentes para a mesma espécie", "Sucuri é menor", "Anaconda é venenosa", "Sucuri vive na água"], "correct": 0, "difficulty": "medium"},
    {"animal": "Sucuri", "question": "Qual o nome científico da sucuri?", "options": ["Eunectes murinus", "Boa constrictor", "Python molurus", "Naja naja"], "correct": 0, "difficulty": "hard"},
    {"animal": "Sucuri", "question": "Como a sucuri reproduz?", "options": ["Ovípara", "Vivípara", "Ovovivípara", "Assexuada"], "correct": 0, "difficulty": "hard"},
    {"animal": "Sucuri", "question": "Quantos filhotes tem em média por ninhada?", "options": ["20-40", "5-10", "50-60", "1-2"], "correct": 0, "difficulty": "hard"},
]

# ==============================
# Difficulty Adjustment Function (Dawkins Style)
# ==============================
def adjust_difficulty(current_difficulty, hits):
    if hits == 3:
        if current_difficulty == "easy":
            return "medium"
        elif current_difficulty == "medium":
            return "hard"
        else:
            return "hard"
    elif hits == 2:
        return current_difficulty
    else:  # 0 or 1 hit
        if current_difficulty == "hard":
            return "medium"
        elif current_difficulty == "medium":
            return "easy"
        else:
            return "easy"

# ==============================
# Map for codes
# ==============================
difficulty_map = {"easy": "000", "medium": "010", "hard": "111"}

# ==============================
# Quiz Execution
# ==============================
def run_quiz():
    print(f"\n--- Iniciando o Quiz ---\n")
    total_hits = 0
    current_difficulty = "easy"

    # Select animals for the game
    quiz_animals = random.sample(animals, 3)

    for round_idx, current_animal in enumerate(quiz_animals, start=1):
        print(f"\n--- Rodada {round_idx}: {current_animal} ---")
        round_hits = 0

        # Select 3 questions of the current difficulty
        level_questions = [q for q in questions if q["animal"] == current_animal and q["difficulty"] == current_difficulty]
        if len(level_questions) < 3:
            level_questions = random.sample([q for q in questions if q["animal"] == current_animal], 3)
        else:
            level_questions = random.sample(level_questions, 3)

        for q in level_questions:
            print(f"\nPergunta ({q['difficulty']}): {q['question']}")
            for i, option in enumerate(q['options']):
                print(f"  {i+1}) {option}")
            answer = input("Sua resposta: ")
            if answer.isdigit() and int(answer)-1 == q['correct']:
                print("✅ Correto!")
                round_hits += 1
            else:
                print(f"❌ Errado! Resposta correta: {q['options'][q['correct']]}\n")

        total_hits += round_hits
        current_difficulty = adjust_difficulty(current_difficulty, round_hits)

        # Evaluation code
        code = f"{str(round_hits).zfill(3)}{difficulty_map[current_difficulty]}"
        print(f"\n📊 Resultado da rodada {round_idx}: {round_hits}/3 acertos")
        print(f"Código de Avaliação: {code}")

    print("\n=== Resultado Final ===")
    print(f"Total de acertos: {total_hits}/{len(quiz_animals)*3}")

# ==============================
# Instructions and Menu
# ==============================
def show_instructions():
    print("\n📘 Instruções do Quiz:")
    print("- Cada rodada traz 3 perguntas de um animal")
    print("- Cada animal tem 9 perguntas (3 fáceis, 3 médias e 3 difíceis)")
    print("- A dificuldade se adapta ao seu desempenho, como no experimento da Doninha de Dawkins")
    print("- Código de Avaliação: 3 dígitos de acertos + 3 dígitos de dificuldade (000, 010, 111)\n")

def interactive_menu():
    while True:
        print("\n===== CIGS Zoo Weasel Quiz =====")
        print("1 - Iniciar Quiz")
        print("2 - Instruções")
        print("3 - Sair")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            run_quiz()
        elif choice == "2":
            show_instructions()
        elif choice == "3":
            print("👋 Saindo do quiz. Até a próxima!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    interactive_menu()