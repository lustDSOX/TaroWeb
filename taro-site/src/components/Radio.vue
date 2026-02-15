<script>
export default {
  props: {
    modelValue: {
      type: String,
      required: true
    },
    value: {
      type: String,
      default: false
    },
    label: {
      type: String,
      required: true
    },
    description : {
      type: String,
    }
  },
  emits: ['update:modelValue']
}
</script>

<template>
  <label
      class="w-full sm:w-64 md:w-72 min-h-auto p-4 sm:p-6 cursor-pointer border transition-all duration-200 flex flex-col"
      :class="modelValue === value ? 'border-[#B7A18A]' : 'border-transparent hover:border-[#8C8A80]'"
  >
    <input
        type="radio"
        class="hidden"
        :name="name"
        :value="value"
        :checked="modelValue === value"
        @change="$emit('update:modelValue', value)"
    />

    <span class="flex flex-col mt-2">
    <span class="text-[#00010D] text-xl sm:text-2xl md:text-3xl">{{label}}</span>
    <span class="text-[#8C8A80] text-base sm:text-lg md:text-2xl">{{description}}</span>
  </span>
  </label>
</template>

<style scoped>

</style>