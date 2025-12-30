import fs from 'fs';
import toml from 'toml';

export type Suit = 'c' | 'd' | 'h' | 's';
export type Rank = '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'T' | 'J' | 'Q' | 'K' | 'A';
export const RANKS: Rank[] = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

export type Action = {
    name: string;
    amount?: number;
}

export type HandAction = {
    action: Action;
    freq: number;
}

const RANGES = {
  utg_rfi_30bb: () => import('$lib/assets/ranges/utg_rfi_30bb.toml?raw'),
  utg1_rfi_30bb: () => import('$lib/assets/ranges/utg1_rfi_30bb.toml?raw'),
  mp_rfi_30bb: () => import('$lib/assets/ranges/mp_rfi_30bb.toml?raw'),
  hj_rfi_30bb: () => import('$lib/assets/ranges/hj_rfi_30bb.toml?raw'),
  co_rfi_30bb: () => import('$lib/assets/ranges/co_rfi_30bb.toml?raw'),
  btn_rfi_30bb: () => import('$lib/assets/ranges/btn_rfi_30bb.toml?raw'),
  sb_rfi_30bb: () => import('$lib/assets/ranges/sb_rfi_30bb.toml?raw'),
};

export const Ranges = Object.keys(RANGES);
export const Positions = [
    'SB',
    'BB',
    'UTG',
    'UTG1',
    'MP',
    'HJ',
    'CO',
    'BTN',
];
export const Actions = [
    'RFI',
];
export const StackSizes = [
    '30bb',
];


export class Range {
    position: string;
    action: string;
    stackSize: string;
    strategy: Record<string, HandAction[]> = {};

    private constructor(position: string, action: string, stackSize: string, strategy: Record<string, HandAction[]>) {
        this.position = position;
        this.action = action;
        this.stackSize = stackSize;
        this.strategy = strategy;
    }

    static parseStrategy(data: Record<string, any>): Record<string, HandAction[]> {
        return Object.fromEntries(
            Object.entries(data)
                .filter(([hand]) => hand !== 'meta')
                .map(([hand, actions]) => [
                    hand,
                    actions.map((a: any) => ({
                        action: { name: a.action, amount: a.amount },
                        freq: a.freq
                    }))
                ])
        );
    }

    static async create(name: keyof typeof RANGES): Promise<Range> {
        const module = await RANGES[name]();
        const text = module.default;
        const data = toml.parse(text) as Record<string, any>;
        return new Range(
            data['meta']['position'],
            data['meta']['action'],
            data['meta']['stack'],
            this.parseStrategy(data),
        );
    }

    name() {
        return this.position + ' ' + this.action + ' ' + this.stackSize
    }

    get(hand: string) {
        return this.strategy[hand];
    }
}
