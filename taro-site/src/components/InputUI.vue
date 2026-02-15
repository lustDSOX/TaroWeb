<script>
export default {
  props: {
    modelValue : {
      type: String,
      default: ()=> '',
    }
  }
}
</script>

<template>
  <textarea type="text" class="w-full border-[#8C8A80] border-1 p-4 text-[#8C8A80] focus:border-0 resize-none" placeholder="Напишите свою историю" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"></textarea>
</template>

<style scoped>

</style>