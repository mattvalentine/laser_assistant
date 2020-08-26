<template>
  <div class="jointparams" :display="show">
    <div class="jointoptions">
      Joint type
      <select name="jointtype" v-model="jp.joint_type">
        <option disabled value>Please select one</option>
        <option>Box</option>
        <option>Tab-and-Slot</option>
        <option>Interlocking</option>
        <option>Bolt</option>
        <!-- <option>C</option> -->
      </select>
      Fit
      <select name="fit" v-model="jp.fit">
        <option disabled value>Please select one</option>
        <option>Clearance</option>
        <option>Friction</option>
        <option>Press</option>
        <!-- <option>C</option> -->
      </select>
      Tab Size(mm)
      <input name="tabsize" v-model="jp.tabsize" type="number" step="1.0" />
      Tab Spacing(mm)
      <input name="tabspace" v-model="jp.tabspace" type="number" step="1.0" />
      Number of Tabs
      <input name="tabnum" v-model="jp.tabnum" type="number" step="1" />
      <div id="flipjoint">
        <button @click="flipjoint">Reverse Joint</button>
      </div>
      <div id="applyjoint">
        <button @click="confirmjoint">Apply</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "JointParams",
  props: ["show", "setjp"],
  data: function () {
    return {
      jp: this.setjp,
    };
  },
  watch: {
    setjp: function (updatedjp) {
      this.jp = updatedjp;
    },
  },
  methods: {
    confirmjoint: function () {
      console.log("confirm");
      this.jp.tabsize = parseFloat(this.jp.tabsize);
      this.jp.tabspace = parseFloat(this.jp.tabspace);
      this.jp.tabnum = parseInt(this.jp.tabnum);
      this.$emit("confirm", this.jp);
    },
    flipjoint: function () {
      this.$emit("flipjoint");
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
  /* cursor: pointer; */
  /* line-height: 3vmin; */
  display: grid;
  grid-template-columns: 50% 50%;
  grid-gap: 5px;
}
#applyjoint {
  grid-column: 1/3;
  display: flex;
  align-items: center;
  justify-content: center;
  /* width: 200px; */
}
#applyjoint > button {
  padding: 5px;
}
</style>