import { IFrame } from '@jupyterlab/apputils';
import { URLExt, PageConfig } from '@jupyterlab/coreutils';
import { IFlameGraph, SPEEDSCOPE_HTML_URL, STYLE } from './tokens';

const LABEXT_URL = PageConfig.getOption('fullLabextensionsUrl');

import '../style/index.css';

const SANDBOX: IFrame.SandboxExceptions[] = ['allow-scripts'];

export class FlamegraphPanel extends IFrame {
  protected _options: Partial<IFlameGraph.IOptions> | null = null;
  protected _speedscopeUrl: string | null = null;

  constructor(options?: FlamegraphPanel.IOptions) {
    super({ ...options, sandbox: SANDBOX });
    this.addClass(STYLE.panel);
    this.options = options?.speedscopeOptions || null;
  }

  get options(): Partial<IFlameGraph.IOptions> | null {
    return this._options;
  }

  set options(options: Partial<IFlameGraph.IOptions> | null) {
    this._options = options;
    this.url = 'about:blank';
    setTimeout(() => {
      const newUrl = this.speedscopeUrl;
      if (this.url !== newUrl) {
        this.url = newUrl;
      }
    }, 10);
  }

  protected get speedscopeUrl(): string {
    let hash = '';
    const { options } = this;
    if (options) {
      const params: Record<string, string> = {};
      for (let [key, value] of Object.entries(options)) {
        if (value == null) {
          continue;
        }
        if (key == 'profile') {
          key = 'profileURL';
          value = `data:application/json;base64,${btoa(value)}`;
        }
        params[key] = value;
      }
      hash = '#' + URLExt.objectToQueryString(params).slice(1);
    }
    return URLExt.join(LABEXT_URL, SPEEDSCOPE_HTML_URL) + hash;
  }
}

export namespace FlamegraphPanel {
  export interface IOptions extends IFrame.IOptions {
    speedscopeOptions?: Partial<IFlameGraph.IOptions>;
  }
}
