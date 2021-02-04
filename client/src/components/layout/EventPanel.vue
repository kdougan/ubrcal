<template>
  <div class="event-card card">
    <div class="card-image">
      <figure class="image is-2by1">
        <img
          src="https://bulma.io/images/placeholders/640x320.png"
          alt="Placeholder image"
        />
      </figure>
      <div class="card-image-overlay">
        <div class="card-overlay-header">
          <b-image
            src="https://bulma.io/images/placeholders/128x128.png"
            alt="user alias"
            class="is-128x128 avatar m-5"
            rounded
          />
          <div class="date-badge mx-5 p-2 is-dark has-background-primary">
            <div class="day title has-text-primary-light">1</div>
            <div class="month is-uppercase subtitle has-text-primary-light">
              Jan
            </div>
          </div>
        </div>
        <div
          class="event-context subtitle px-4 py-2 has-text-light has-text-weight-semibold is-uppercase"
        >
          playing a game
        </div>
      </div>
    </div>
    <div
      class="card-content-header has-background-primary has-text-white is-uppercase has-text-weight-bold p-2 has-text-centered"
    >
      <span class="px-2">Saturday, January 1st @ 12:00 PM</span
      ><span class="px-2">Duration: 1 HR</span>
    </div>
    <div class="card-content">
      <div class="event-title title">This is the title of the event</div>
      <div class="event-timer subtitle has-text-primary mb-1">in 6 minutes</div>
      <b-tabs position="is-centered" class="block">
        <b-tab-item label="Description">
          Reprehenderit aliqua et consectetur elit do enim enim dolore proident
          velit amet eiusmod. Ullamco proident aliqua adipisicing deserunt
          proident in nulla do Lorem enim elit. Ad et culpa dolor cupidatat
          voluptate. Incididunt elit duis aliquip nulla. <br />
          Ullamco anim nulla dolor duis laboris. Id elit elit pariatur et
          cupidatat excepteur id id duis. Ad est labore nisi cupidatat minim ad
          aliquip labore aliquip irure quis do excepteur culpa. <br />
          Sint ut sint nulla velit. Aliquip Lorem sunt deserunt ad. Nisi
          occaecat voluptate irure mollit aute ipsum enim velit dolor voluptate
          nostrud deserunt dolor veniam. Esse nostrud qui minim veniam velit.
          Exercitation reprehenderit anim cillum nulla duis. Officia irure elit
          elit ipsum deserunt fugiat quis anim non sit dolor aliquip. <br />
          <b-collapse
            :open="false"
            position="is-bottom"
            aria-id="contentIdForA11y1"
          >
            <template #trigger="props">
              <a aria-controls="contentIdForA11y1">
                <b-icon :icon="!props.open ? 'menu-down' : 'menu-up'"></b-icon>
                {{ !props.open ? 'more' : 'less' }}
              </a>
            </template>
            Do mollit cupidatat minim cillum adipisicing laboris proident sunt
            Lorem. Ad consequat voluptate excepteur dolor eu nisi. Magna
            proident anim enim id id Lorem aliqua commodo quis minim. Irure aute
            proident quis proident ullamco mollit Lorem. <br />
            Dolor aliquip excepteur occaecat non esse irure enim aute duis. Ad
            qui nulla sunt adipisicing proident irure nostrud laboris tempor
            cupidatat eu. Voluptate sunt enim aute est et laborum ea incididunt
            reprehenderit veniam cupidatat magna fugiat in. Enim aliquip minim
            dolor Lorem est id laboris consectetur ea dolore veniam dolore
            nostrud. Occaecat nisi laborum et reprehenderit duis. Eiusmod id non
            sit adipisicing enim est ipsum fugiat tempor minim aliqua.
            Exercitation velit sint consequat esse anim dolor in magna sint.
            <br />
            Enim exercitation sunt sit qui. Ut fugiat deserunt ex ad adipisicing
            aliqua minim reprehenderit ipsum aute ex consectetur aliquip. Ex
            esse nisi velit quis. Voluptate anim esse sit velit est consectetur
            fugiat do. Occaecat exercitation laboris consectetur nulla in. Id
            consectetur quis aliqua est proident id non ex. <br />
            Sit occaecat deserunt do incididunt occaecat consequat excepteur
            consequat laborum nulla cupidatat mollit. Fugiat laborum fugiat
            laboris proident. Fugiat aliqua quis consectetur cupidatat enim ex
            tempor ut incididunt aliquip magna anim reprehenderit laborum. Ipsum
            irure in deserunt eu laborum amet laboris cillum in. Nostrud
            occaecat elit minim exercitation amet ut commodo voluptate nulla
            amet officia. Ad sint tempor incididunt dolore. Minim id veniam ut
            non irure nulla anim sint eiusmod consectetur voluptate. <br />
            Commodo culpa elit laboris dolor elit aliquip cillum magna ex ut
            sunt laboris. Fugiat excepteur exercitation occaecat duis irure
            adipisicing deserunt enim consectetur sint voluptate consequat do.
            Proident deserunt ad minim velit eu exercitation sunt amet.
            Exercitation ut veniam ipsum officia mollit. Dolore in deserunt
            incididunt fugiat.
            <br />
            Occaecat eu eu deserunt est quis mollit irure duis. In dolor
            cupidatat id non ad adipisicing eiusmod id aute labore ipsum
            proident. Est eiusmod anim non labore dolor ex eiusmod velit nisi.
            Laborum aliquip laboris commodo irure sunt labore deserunt quis.
            Pariatur enim excepteur proident ea eu sit reprehenderit est amet do
            voluptate.
            <br />
            Reprehenderit reprehenderit laborum ut enim sunt duis sint ut esse
            sint ut ea dolore deserunt. Sit dolore esse duis incididunt tempor
            sunt voluptate. Anim nostrud sint aliquip labore ea elit ipsum nulla
            sit non veniam et do. Ad dolore nulla laboris qui irure esse cillum
            magna laboris eu nostrud occaecat velit ut. Veniam ex aute pariatur
            adipisicing sint ullamco irure ullamco. Est sit id consequat amet
            nostrud nulla aliqua sit ea tempor labore tempor officia mollit.
            Dolor duis proident esse ad labore exercitation consequat irure
            tempor aute ipsum amet enim ea.
          </b-collapse>
        </b-tab-item>
        <b-tab-item label="Groups">
          <div class="card-group-content">
            <div class="group mb-4">
              <span class="group-name subtitle">Group 1</span>
              <div class="group-content">
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
              </div>
            </div>
            <div class="group">
              <span class="group-name subtitle">Group 2</span>
              <div class="group-content">
                <b-image
                  src="https://bulma.io/images/placeholders/64x64.png"
                  alt="user alias"
                  class="is-64x64 avatar m-2"
                  rounded
                />
              </div>
            </div>
          </div>
        </b-tab-item>
      </b-tabs>
    </div>
    <footer class="card-footer px-4 py-1">
      <span class="icon-text">
        <span class="icon">
          <i class="mdi mdi-account-group"></i>
        </span>
        <span>4 participants</span>
      </span>
      <span class="icon-text">
        <span class="icon">
          <i class="mdi mdi-bell"></i>
        </span>
        <span>120 reminters set</span>
      </span>
    </footer>
  </div>
</template>

<script>
export default {
  data: () => {
    return {};
  },
};
</script>

<style lang="scss">
.event-card {
  display: flex;
  flex-direction: column;
  width: 100%;

  .card-content {
    flex-grow: 1;
    overflow-y: auto;
  }

  .card-content-header {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
  }

  .card-group-content {
    .group-content {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      .avatar img {
        box-shadow: 0 0 0.5rem -0.25rem rgba(0, 0, 0, 0.5);
      }
    }
  }
}

.card-image {
  position: relative;

  .card-image-overlay {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0;

    .card-overlay-header {
      display: flex;
      flex-direction: row;
      flex-grow: 1;
      justify-content: space-between;
    }

    .avatar img {
      box-shadow: 0 0 0.5rem -0.25rem rgba(0, 0, 0, 0.5),
        0 0 1rem rgba(0, 0, 0, 0.5);
    }

    .date-badge {
      display: flex;
      flex-direction: column;
      align-items: stretch;
      text-align: center;
      height: 7rem;
      width: 4rem;

      .day {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        flex-grow: 1;
      }
    }
    .event-context {
      width: 100%;
      background-color: rgba(0, 0, 0, 0.45);
    }
  }
}
</style>