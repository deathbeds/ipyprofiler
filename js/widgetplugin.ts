import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { NAME, VERSION } from './tokens';

export const widgetPlugin: IPlugin<Application<Widget>, void> = {
  id: `${NAME}:widgets`,
  requires: [IJupyterWidgetRegistry],
  autoStart: true,
  activate: (_: Application<Widget>, registry: IJupyterWidgetRegistry) => {
    const reg = {
      name: NAME,
      version: VERSION,
      exports: async () => import('./widgets'),
    };
    registry.registerWidget(reg);
  },
};
