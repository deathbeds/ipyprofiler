import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IFlameGraph, NAME } from './tokens';
import { widgetPlugin } from './widgetplugin';

async function activate(app: JupyterFrontEnd): Promise<IFlameGraph> {
  return {};
}

const plugin: JupyterFrontEndPlugin<IFlameGraph> = {
  id: `${NAME}:IFlameGraph`,
  activate,
  autoStart: true,
  provides: IFlameGraph,
};

const plugins = [plugin, widgetPlugin];

export default plugins;
