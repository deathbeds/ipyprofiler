import { BoxModel, BoxView } from '@jupyter-widgets/controls';
import { FlamegraphPanel } from './renderer';
import { NAME, VERSION, STYLE, WIDGET_DEFAULTS } from './tokens';

import {
  DOMWidgetModel,
  DOMWidgetView,
  unpack_models as deserialize,
} from '@jupyter-widgets/base';

export class ProfileJSONModel extends DOMWidgetModel {
  static model_name = 'ProfileJSONModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'ProfileJSONView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults,
      ...WIDGET_DEFAULTS,
      _model_name: ProfileJSONModel.model_name,
      _view_name: ProfileJSONModel.view_name,
    };
  }
}

export class ProfileJSONView extends DOMWidgetView {
  protected _pre: HTMLPreElement | null = null;

  initialize(parameters: any) {
    super.initialize(parameters);
    this.el.classList.add(STYLE.widgetFileView);
    this.update();
  }

  update() {
    let { _pre } = this;
    if (_pre == null) {
      _pre = this._pre = document.createElement('pre');
      this.el.appendChild(this._pre);
    }

    _pre.innerHTML = this.model.get('value') || 'None';
  }
}

export class FlamegraphModel extends BoxModel {
  static model_name = 'FlamegraphModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'FlamegraphView';
  static view_module = NAME;
  static view_module_version = VERSION;
  static serializers = { ...BoxModel.serializers, profile: { deserialize } };

  defaults() {
    return {
      ...super.defaults(),
      ...WIDGET_DEFAULTS,
      _model_name: FlamegraphModel.model_name,
      _view_name: FlamegraphModel.view_name,
      view: null,
      profile: null,
      title: null,
    };
  }
}

export class FlamegraphView extends BoxView {
  protected _panel: FlamegraphPanel | null = null;

  protected get flamegraphModel(): FlamegraphModel {
    return this.model as FlamegraphModel;
  }

  render() {
    super.render();
    this.el.classList.add(STYLE.widgetView);
    this.flamegraphModel.on('change:profile', this.onProfileChange, this);
    this.flamegraphModel.on('change:view', this.onModelChange, this);
    this.onProfileChange();
  }

  protected onProfileChange(): void {
    const oldProfile = this.model.previous('profile');
    if (oldProfile instanceof ProfileJSONModel) {
      oldProfile.off('change:value', this.onModelChange, this);
    }
    const profile = this.model.get('profile');
    if (profile instanceof ProfileJSONModel) {
      profile.on('change:value', this.onModelChange, this);
    }
    this.onModelChange();
  }

  protected onModelChange(): void {
    let { _panel, flamegraphModel } = this;
    if (!_panel) {
      _panel = this._panel = new FlamegraphPanel();
      (this.luminoWidget || this.pWidget).addWidget(_panel);
    }
    const profile = flamegraphModel.get('profile')?.get('value') || null;
    const view = flamegraphModel.get('view');
    _panel.options = { profile, view };
  }
}
