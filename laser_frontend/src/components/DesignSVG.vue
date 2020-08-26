<template>
  <div id="designsvg" class="design model" v-html="designsvg"></div>
</template>

<script>
export default {
  name: "DesignSVG",
  props: ["designsvg"],
};
</script>

<style>
.design {
  z-index: 0;
}

.design > svg {
  width: 100%;
}
</style>