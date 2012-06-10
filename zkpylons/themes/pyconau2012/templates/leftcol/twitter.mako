<div style="padding: 0.5em">
<script charset="utf-8" src="http://widgets.twimg.com/j/2/widget.js"></script>
<script>
new TWTR.Widget({
  version: 2,
  type: 'profile',
  search: 'pyconau',
  rpp: 4,
  interval: 10000,
  title: '',
  subject: '#pyconau',
  width: 'auto',
  height: 300,
  theme: {
    shell: {
      background: '#3d91d6',
      color: '#ffffff'
    },
    tweets: {
      background: '#ffffff',
      color: '#444444',
      links: '#03008F'
    }
  },
  features: {
    scrollbar: true,
    loop: false,
    live: true,
    behavior: 'all'
  }
}).render().setUser('pyconau').start();
</script></div>
