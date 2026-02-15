<script>
import Radio from "@/components/Radio.vue";
import InputUI from "@/components/InputUI.vue";
import ButtonUi from "@/components/ButtonUi.vue";
import Alert from "@/components/Alert.vue";

export default {
  components: {
    Alert,
    Radio, InputUI, ButtonUi
  },
  data() {
    return {
      selectedOption: null,
      inputStory: '',
      optionValue: '',
      data: [],
      fullAnswer: '',
      cards: [],
      openAlert: false
    }
  },

  methods: {
    async getSituation() {

      if (!this.selectedOption || this.inputStory == null) {
        this.openWindow()
      }
      try {
        const params = new URLSearchParams({
          option: this.selectedOption,
          query: this.inputStory,
        })

        const response = await fetch(`/api/tarot?${params.toString()}`)

        // чтобы почистить ответ от модели
        let correctAllAnswer = ''

        if (!response.ok) {
          const errorText = await response.text()
          console.log("Статус:", response.status)
          console.log("Ответ сервера:", errorText)
          throw new Error(`Ошибка ${response.status}`)
        }

        if (!response.body) {
          throw new Error("ошибка в теле запроса")
        }

        // поскольку идет "стрим" во время ответа, то необходимо создать "читателя" и декодера для него
        const reader = response.body.getReader() //считывает стрим
        const decoder = new TextDecoder() //декодирует каждый байт

        // очищает каждый ответ
        let buffer = ""
        this.fullAnswer = ""
        this.cards = []

        while (true) {
          const {value, done} = await reader.read()

          if (done) {
            break
          }

          // так как json приходит в формате таком, что data: {"answer_chunk": то необходимо соединить каждую строчку(чанк) в одну и удалить ненужные пробелы
          buffer += decoder.decode(value, { stream: true })

          const events = buffer.split("\n\n")
          buffer = events.pop()

          for (const event of events) {
            const line = event.split("\n\n").find(l => l.startsWith("data:"))

            if (!line) continue

            const json = line.replace("data:", "").trim()
            const parsed = JSON.parse(json)

            if (parsed.answer_chunk) {
              correctAllAnswer += parsed.answer_chunk
              this.fullAnswer = this.clearText(correctAllAnswer)
            }

            parsed.cards?.forEach(card => this.cards.push(card))
            console.log(this.cards)
          }
        }
      } catch (err) {
        console.error("ошибка", err)
      }

    },

    clearText(answer) {
      answer = answer.replace(/[#*]/g, '')

      if (answer.startsWith('Вариант')) {
        answer = answer.replace(/Вариант\s+[А-ЯA-Z]:?/gi, '\n$&');
      }
      return answer
    },

    openWindow() {
        this.openAlert = true
    }
  }
}
</script>

<template>
  <div class="header">
    <div class="logo">
        <div class="sun-logo">
          <img class="sun_lines" src="/img/sun_lines.svg">
          <img class="sun_face" src="/img/face.svg">
        </div>
    </div>

    <p class="text-[#0D0D0D] text-4xl text-center mt-8 mb-8">Получи ответы на все вопросы</p>

    <alert :openAlert="openAlert">Поля обязательны для заполнения</alert>

    <div class="cards">
      <div class="card mt-2">
        <div class="cards flex justify-between flex-col sm:flex-row gap-4 items-stretch sm:items-start">
          <Radio
              v-model="selectedOption"
              value="linear"
              label="Линейный расклад"
              description="Узнать настоящее, прошлое и будущее"
          />
          <Radio
              v-model="selectedOption"
              value="balance"
              label="Расклад Баланс"
              description="Расклад из 4 карт. Что поддерживает вас, что влияет извне, что нарушает равновесие, как восстановить баланс"
          />
          <Radio
              v-model="selectedOption"
              value="advice"
              label="Расклад Баланс"
              description="Расклад из 2 карт. Что, например, сделать и чего стоит избегать"
          />
        </div>
      </div>
    </div>

    <div class="story w-full mt-8">
      <input-u-i v-model="inputStory"></input-u-i>
    </div>


    <div class="btn flex justify-center mt-8">
      <button-ui @click="getSituation">Рассчитать</button-ui>
    </div>

  </div>
    <div class="full-answer text-[#00010D] text-center mt-[5vh]">
      {{fullAnswer}}
    </div>

  <div class="card-section flex justify-between items-center flex-col sm:flex-row gap-4 sm:gap-6 items-stretch">
    <div class="cards mt-[5vh]" v-for="card in cards">
      <div class="img">
        <img :src="card.image" id="image-taro" class='w-3xs sm:w-2xs'></img>
      </div>
      <div class="name text-center mt-2">
        <label for="image-taro">{{card.name}}</label>
      </div>
    </div>
  </div>




</template>

<style scoped>

</style>
