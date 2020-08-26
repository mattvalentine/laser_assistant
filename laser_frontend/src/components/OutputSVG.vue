<template>
  <div id="outputsvg" class="output model" v-html="outsvg"></div>
</template>

<script>
export default {
  name: "OutputSVG",
  props: ["outsvg"],
};
</script>

<style>
.output {
  z-index: 1;
}

.output > svg {
  width: 100%;
}
</style>
