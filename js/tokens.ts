import _PKG from '../package.json';

const PKG = _PKG;

export const NAME = PKG.name;
export const VERSION = PKG.version;

import { Token } from '@lumino/coreutils';

export interface IFlameGraph {
  // nothing here yet.
}

export const IFlameGraph = new Token<IFlameGraph>(`${NAME}:plugin`);

export const SPEEDSCOPE_HTML_URL = `${NAME}/static/speedscope/index.html`;

export namespace IFlameGraph {
  export type TView = 'time-ordered' | 'left-heavy' | 'sandwich';
  export interface IOptions {
    /** a human-readable title */
    title: string | null;
    /** the JSON for a profile */
    profile: string | null;
    /** the current view setting */
    view: IFlameGraph.TView;
  }
}

export namespace STYLE {
  const _base = 'jprf-Flamegraph';
  export const panel = `${_base}Panel`;
  export const widgetView = `${_base}View`;
  export const widgetFileView = `${_base}FileView`;
}

export const WIDGET_DEFAULTS = {
  _model_module: NAME,
  _model_module_version: `^${VERSION}`,
  _view_module: NAME,
  _view_module_version: `^${VERSION}`,
};
