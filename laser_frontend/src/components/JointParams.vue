<template>
  <div class="jointparams" :display="show">
    <div class="jointoptions" @click="confirmjoint">
      joint type
      <br />params
      <br />params
      <br />params
      <br />params
    </div>
  </div>
</template>

<script>
export default {
  name: "JointParams",
  props: ["show"],
  methods: {
    confirmjoint: function () {
      console.log("confirm");
      this.$emit("confirm", { some: "junk" });
    },
  },
};
</script>

<style>
.jointparams {
  z-index: 20;
  grid-area: svg;
  /* background-color: red; */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.jointoptions {
  background: lightgray;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 1px 4px rgba(0, 0, 0, 0.4);
  cursor: pointer;
}
</style>