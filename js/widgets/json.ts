import { NAME, STYLE, VERSION, WIDGET_DEFAULTS } from '../tokens';

import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';

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
      value: null,
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
