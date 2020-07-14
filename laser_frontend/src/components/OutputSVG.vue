<template>
  <div class="output" v-html="outsvg"></div>
</template>

<script>
export default {
  name: "OutputSVG",
  props: ["outsvg"]
};
</script>

<style>
.output {
  grid-column: 1 / 4;
  grid-row: 1;
  display: grid;
  align-items: center;
  z-index: 0;
  width: 100%;
}

.output > svg {
  width: 100%;
}
</style>
